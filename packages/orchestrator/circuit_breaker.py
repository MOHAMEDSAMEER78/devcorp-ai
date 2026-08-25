"""Circuit Breaker & Infinite Loop Guard for Autonomous Swarm Execution."""
import hashlib
from typing import Dict, Any, Tuple


class SwarmCircuitBreaker:
    """Enforces deterministic iteration limits and semantic oscillation protection."""

    def __init__(self, max_retries_per_ticket: int = 5):
        self.max_retries = max_retries_per_ticket
        self.code_hash_history: Dict[str, list[str]] = {}

    def compute_code_hash(self, code_diff: str) -> str:
        """Compute SHA256 hash of a code diff or AST representation."""
        return hashlib.sha256(code_diff.encode("utf-8")).hexdigest()

    def check_ticket_retry(self, ticket_id: str, current_retries: int) -> Tuple[bool, str]:
        """Check if a ticket has exceeded retry limits.
        
        Returns:
            (is_tripped: bool, reason: str)
        """
        if current_retries >= self.max_retries:
            return True, f"Ticket {ticket_id} reached maximum retry limit ({self.max_retries}). Escalating to Engineering Manager."
        return False, "OK"

    def record_and_check_oscillation(self, ticket_id: str, code_diff: str) -> Tuple[bool, str]:
        """Detect circular syntax oscillations (agent flipping between identical edits)."""
        c_hash = self.compute_code_hash(code_diff)
        history = self.code_hash_history.setdefault(ticket_id, [])

        if c_hash in history[-3:]:  # Observed identical hash within last 3 iterations
            return True, f"Semantic oscillation detected on ticket {ticket_id}: repeated code state hash {c_hash}."

        history.append(c_hash)
        return False, "OK"
