"""Autonomous Agent Execution Runtime (ReAct Tool Loop & Trajectory Logging)."""
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from packages.mcp_servers.filesystem_server import FilesystemServer
from packages.mcp_servers.terminal_server import TerminalServer
from .prompt_loader import PromptLoader

logger = logging.getLogger(__name__)


class AgentTrajectoryLogger:
    """Maintains append-only trajectory event logs for auditability and replay."""

    def __init__(self, role_name: str, base_dir: str = "trajectories"):
        self.role_name = role_name
        self.log_dir = Path(base_dir) / role_name
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "trajectory.jsonl"

    def log_step(self, step_number: int, action: str, details: Any) -> None:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "role": self.role_name,
            "step": step_number,
            "action": action,
            "details": details
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")


class AutonomousAgentRuntime:
    """ReAct / Tool execution runtime for Tier 4 specialist engineers."""

    def __init__(self, role_name: str, workspace_root: str = "workspace"):
        self.role_name = role_name
        self.workspace_root = Path(workspace_root).resolve()
        self.workspace_root.mkdir(parents=True, exist_ok=True)

        self.fs = FilesystemServer(str(self.workspace_root))
        self.term = TerminalServer()
        self.trajectory = AgentTrajectoryLogger(role_name)
        self.prompt_loader = PromptLoader()

    def write_code_file(self, rel_path: str, code_content: str) -> str:
        """Write real source code file into the target project workspace."""
        res = self.fs.write_file(rel_path, code_content)
        self.trajectory.log_step(
            step_number=1,
            action="mcp.filesystem.write_file",
            details={"file": rel_path, "bytes": len(code_content)}
        )
        return res

    def read_code_file(self, rel_path: str) -> str:
        """Read source code file from target project workspace."""
        content = self.fs.read_file(rel_path)
        self.trajectory.log_step(
            step_number=2,
            action="mcp.filesystem.read_file",
            details={"file": rel_path}
        )
        return content

    def execute_terminal(self, command: str) -> Dict[str, Any]:
        """Execute sandboxed bash command within the target workspace."""
        # Ensure command executes in workspace root
        cmd = f"cd '{self.workspace_root}' && {command}"
        res = self.term.run_command(cmd)
        self.trajectory.log_step(
            step_number=3,
            action="mcp.terminal.run_command",
            details={"command": command, "exit_code": res["exit_code"]}
        )
        return res
