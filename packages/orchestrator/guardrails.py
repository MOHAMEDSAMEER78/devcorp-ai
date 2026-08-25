"""Operational Guardrails, Hallucination Traps, and Security Policies."""
import logging
from typing import Dict, Any, List, Tuple, Optional
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class SwarmGuardrailManager:
    """Detects semantic drift, contract violations, and execution anomalies."""

    def validate_schema_compliance(self, payload: Dict[str, Any], schema_cls: Any) -> Tuple[bool, Optional[str]]:
        """Verify that an artifact strictly adheres to its Pydantic contract."""
        try:
            schema_cls.model_validate(payload)
            return True, None
        except ValidationError as e:
            logger.error(f"Schema contract violation: {e}")
            return False, str(e)

    def verify_no_sandbox_escape(self, bash_command: str) -> Tuple[bool, Optional[str]]:
        """Block forbidden destructive commands or host penetration attempts."""
        forbidden_patterns = [
            "rm -rf /",
            ":(){ :|:& };:",
            "/etc/shadow",
            "chmod -R 777 /",
            "iptables -F",
            "> /dev/sda"
        ]
        for pattern in forbidden_patterns:
            if pattern in bash_command:
                logger.critical(f"Forbidden command detected in sandbox agent script: {pattern}")
                return False, f"Forbidden command pattern '{pattern}' rejected by security guardrail"
        return True, None
