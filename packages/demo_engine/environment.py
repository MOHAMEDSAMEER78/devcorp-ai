"""Ephemeral Application Stack Lifecycle Manager for Demo Recording."""
import socket
import logging
import subprocess
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class EphemeralEnvironment:
    """Manages the lifecycle of temporary local application service stacks for demos."""

    def __init__(self, frontend_port: int = 3000, backend_port: int = 8000):
        self.frontend_port = frontend_port
        self.backend_port = backend_port
        self.processes: list[subprocess.Popen] = []

    def is_port_open(self, host: str, port: int) -> bool:
        """Check if service port is actively accepting connections."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            return s.connect_ex((host, port)) == 0

    def check_health(self) -> Dict[str, bool]:
        return {
            "frontend": self.is_port_open("localhost", self.frontend_port),
            "backend": self.is_port_open("localhost", self.backend_port),
        }

    def teardown(self) -> None:
        """Terminate any background dev processes spawned for the demo."""
        for p in self.processes:
            try:
                p.terminate()
                p.wait(timeout=3)
            except Exception as e:
                logger.warning(f"Error terminating demo process ({e})")
        self.processes.clear()
