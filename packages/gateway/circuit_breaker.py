"""Redis-backed Three-State Circuit Breaker for Inference Gateway Resilience."""
import time
import logging
from enum import Enum
from typing import Optional, Tuple, Any

logger = logging.getLogger(__name__)


class CircuitState(str, Enum):
    CLOSED = "CLOSED"      # Normal Operation (Traffic allowed)
    OPEN = "OPEN"          # Fast-Fail & Divert (Failover tier active)
    HALF_OPEN = "HALF_OPEN"# Probing Recovery (Single test request)


class InferenceCircuitBreaker:
    """Three-state Circuit Breaker pattern protecting agent swarm from provider outages."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout_seconds: float = 60.0,
        redis_client: Optional[Any] = None
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self.redis = redis_client
        
        # Local in-memory state fallback when Redis is absent
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = 0.0

    def get_state(self, provider_name: str = "primary") -> CircuitState:
        now = time.time()

        if self._state == CircuitState.OPEN:
            if (now - self._last_failure_time) >= self.recovery_timeout_seconds:
                logger.info(f"Circuit Breaker for {provider_name}: Cooldown elapsed -> Transitioning to HALF_OPEN (Probing).")
                self._state = CircuitState.HALF_OPEN

        return self._state

    def record_success(self, provider_name: str = "primary") -> None:
        if self._state in (CircuitState.HALF_OPEN, CircuitState.OPEN):
            logger.info(f"Circuit Breaker for {provider_name}: Probe successful -> Transitioning to CLOSED (Normal).")
        self._state = CircuitState.CLOSED
        self._failure_count = 0

    def record_failure(self, provider_name: str = "primary") -> Tuple[CircuitState, str]:
        self._failure_count += 1
        self._last_failure_time = time.time()

        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.OPEN
            logger.warning(f"Circuit Breaker for {provider_name}: Probe failed -> Trip back to OPEN.")
            return CircuitState.OPEN, "Probe request failed during recovery"

        if self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN
            logger.warning(f"Circuit Breaker for {provider_name}: Failure threshold reached ({self._failure_count}) -> Trip to OPEN.")
            return CircuitState.OPEN, f"Breached {self.failure_threshold} consecutive provider failures"

        return self._state, f"Recorded failure ({self._failure_count}/{self.failure_threshold})"
