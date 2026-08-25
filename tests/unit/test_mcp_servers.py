"""Unit tests for MCP Server Implementations."""
import pytest
from packages.mcp_servers import (
    FilesystemServer,
    TerminalServer,
    TestRunnerServer,
)


def test_filesystem_server(tmp_path):
    server = FilesystemServer(root_dir=str(tmp_path))

    # 1. Write file
    resp = server.handle_request({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "write_file",
            "arguments": {"path": "test.txt", "content": "hello mcp"}
        },
        "id": 1
    })
    assert "error" not in resp

    # 2. Read file
    resp = server.handle_request({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "read_file",
            "arguments": {"path": "test.txt"}
        },
        "id": 2
    })
    assert "hello mcp" in resp["result"]["content"][0]["text"]

    # 3. List dir
    resp = server.handle_request({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "list_dir",
            "arguments": {"path": "."}
        },
        "id": 3
    })
    assert "test.txt" in resp["result"]["content"][0]["text"]


def test_terminal_server():
    server = TerminalServer()
    resp = server.handle_request({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "run_command",
            "arguments": {"command": "echo 'devcorp'"}
        },
        "id": 1
    })
    assert "error" not in resp
    assert "devcorp" in resp["result"]["content"][0]["text"]


def test_test_runner_server():
    server = TestRunnerServer()
    resp = server.handle_request({
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 1
    })
    assert len(resp["result"]["tools"]) >= 1
    assert resp["result"]["tools"][0]["name"] == "run_tests"
