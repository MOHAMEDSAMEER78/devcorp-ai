"""MCP Server: Filesystem Tools (JSON-RPC over stdio)."""
import os
import sys
import json
import fnmatch
from pathlib import Path
from typing import Dict, Any, List


class FilesystemServer:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir).resolve()

    def _resolve_path(self, rel_path: str) -> Path:
        resolved = (self.root / rel_path).resolve()
        if not str(resolved).startswith(str(self.root)):
            raise PermissionError(f"Access denied: path {rel_path} outside workspace root {self.root}")
        return resolved

    def read_file(self, path: str) -> str:
        target = self._resolve_path(path)
        with open(target, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self, path: str, content: str) -> str:
        target = self._resolve_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} bytes to {path}"

    def list_dir(self, path: str = ".") -> List[Dict[str, Any]]:
        target = self._resolve_path(path)
        items = []
        for entry in os.scandir(target):
            items.append({
                "name": entry.name,
                "is_dir": entry.is_dir(),
                "size_bytes": entry.stat().st_size if not entry.is_dir() else None,
            })
        return items

    def search_files(self, pattern: str, root_subpath: str = ".") -> List[str]:
        target = self._resolve_path(root_subpath)
        matches = []
        for root, _, filenames in os.walk(target):
            for filename in fnmatch.filter(filenames, pattern):
                full_path = Path(root) / filename
                rel = full_path.relative_to(self.root)
                matches.append(str(rel))
        return matches

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        try:
            if method == "tools/list":
                result = {
                    "tools": [
                        {"name": "read_file", "description": "Read file contents", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
                        {"name": "write_file", "description": "Write or overwrite file contents", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}},
                        {"name": "list_dir", "description": "List directory items", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}}},
                        {"name": "search_files", "description": "Search files matching pattern", "parameters": {"type": "object", "properties": {"pattern": {"type": "string"}, "root_subpath": {"type": "string"}}, "required": ["pattern"]}}
                    ]
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                args = params.get("arguments", {})

                if tool_name == "read_file":
                    res = self.read_file(args["path"])
                elif tool_name == "write_file":
                    res = self.write_file(args["path"], args["content"])
                elif tool_name == "list_dir":
                    res = self.list_dir(args.get("path", "."))
                elif tool_name == "search_files":
                    res = self.search_files(args["pattern"], args.get("root_subpath", "."))
                else:
                    raise ValueError(f"Unknown tool: {tool_name}")
                result = {"content": [{"type": "text", "text": json.dumps(res)}]}
            else:
                raise ValueError(f"Unknown method: {method}")

            return {"jsonrpc": "2.0", "result": result, "id": req_id}
        except Exception as e:
            return {"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": req_id}


def main():
    server = FilesystemServer(os.getcwd())
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        resp = server.handle_request(req)
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
