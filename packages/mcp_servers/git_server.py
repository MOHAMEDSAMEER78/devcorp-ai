"""MCP Server: Git Tools (JSON-RPC over stdio)."""
import sys
import json
import subprocess
from typing import Dict, Any


class GitServer:
    def _run_git(self, args: list[str]) -> str:
        cmd = ["git"] + args
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"Git command failed ({proc.returncode}): {proc.stderr}")
        return proc.stdout

    def status(self) -> str:
        return self._run_git(["status", "--porcelain"])

    def diff(self, staged: bool = False) -> str:
        args = ["diff"]
        if staged:
            args.append("--cached")
        return self._run_git(args)

    def commit(self, message: str) -> str:
        self._run_git(["add", "."])
        return self._run_git(["commit", "-m", message])

    def log(self, max_count: int = 5) -> str:
        return self._run_git(["log", f"-n{max_count}", "--oneline"])

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        try:
            if method == "tools/list":
                result = {
                    "tools": [
                        {"name": "git_status", "description": "Get git status porcelain"},
                        {"name": "git_diff", "description": "Get unstaged or staged git diff", "parameters": {"type": "object", "properties": {"staged": {"type": "boolean"}}}},
                        {"name": "git_commit", "description": "Stage all and commit with message", "parameters": {"type": "object", "properties": {"message": {"type": "string"}}, "required": ["message"]}},
                        {"name": "git_log", "description": "Get recent commit logs", "parameters": {"type": "object", "properties": {"max_count": {"type": "integer"}}}}
                    ]
                }
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})
                if name == "git_status":
                    res = self.status()
                elif name == "git_diff":
                    res = self.diff(args.get("staged", False))
                elif name == "git_commit":
                    res = self.commit(args["message"])
                elif name == "git_log":
                    res = self.log(args.get("max_count", 5))
                else:
                    raise ValueError(f"Unknown git tool: {name}")
                result = {"content": [{"type": "text", "text": res}]}
            else:
                raise ValueError(f"Unknown method: {method}")

            return {"jsonrpc": "2.0", "result": result, "id": req_id}
        except Exception as e:
            return {"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": req_id}


def main():
    server = GitServer()
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        resp = server.handle_request(req)
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
