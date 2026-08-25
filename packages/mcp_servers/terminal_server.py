"""MCP Server: Terminal Execution Tools (JSON-RPC over stdio)."""
import sys
import json
import subprocess
from typing import Dict, Any


class TerminalServer:
    def run_command(self, command: str, timeout_seconds: int = 60) -> Dict[str, Any]:
        proc = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )
        return {
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr
        }

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        try:
            if method == "tools/list":
                result = {
                    "tools": [
                        {
                            "name": "run_command",
                            "description": "Run shell command in sandbox terminal",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "command": {"type": "string"},
                                    "timeout_seconds": {"type": "integer"}
                                },
                                "required": ["command"]
                            }
                        }
                    ]
                }
            elif method == "tools/call":
                if params.get("name") != "run_command":
                    raise ValueError(f"Unknown tool: {params.get('name')}")
                args = params.get("arguments", {})
                res = self.run_command(args["command"], args.get("timeout_seconds", 60))
                result = {"content": [{"type": "text", "text": json.dumps(res)}]}
            else:
                raise ValueError(f"Unknown method: {method}")

            return {"jsonrpc": "2.0", "result": result, "id": req_id}
        except Exception as e:
            return {"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": req_id}


def main():
    server = TerminalServer()
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        resp = server.handle_request(req)
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
