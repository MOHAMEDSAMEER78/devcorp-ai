"""MCP Server: Test Runner & Coverage Tools (JSON-RPC over stdio)."""
import sys
import json
import subprocess
from typing import Dict, Any


class TestRunnerServer:
    def run_tests(self, test_path: str = "tests") -> Dict[str, Any]:
        cmd = f"pytest {test_path} --json-report --json-report-file=/tmp/report.json || pytest {test_path}"
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return {
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "passed": proc.returncode == 0
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
                            "name": "run_tests",
                            "description": "Execute pytest test suite",
                            "parameters": {
                                "type": "object",
                                "properties": {"test_path": {"type": "string"}}
                            }
                        }
                    ]
                }
            elif method == "tools/call":
                if params.get("name") != "run_tests":
                    raise ValueError(f"Unknown tool: {params.get('name')}")
                args = params.get("arguments", {})
                res = self.run_tests(args.get("test_path", "tests"))
                result = {"content": [{"type": "text", "text": json.dumps(res)}]}
            else:
                raise ValueError(f"Unknown method: {method}")

            return {"jsonrpc": "2.0", "result": result, "id": req_id}
        except Exception as e:
            return {"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": req_id}


def main():
    server = TestRunnerServer()
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        resp = server.handle_request(req)
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
