"""Unit tests for Gateway Token Budgets, Circuit Breakers, and Config Generator."""
import pytest
from packages.gateway import (
    BudgetGuardManager,
    RoleBudget,
    InferenceCircuitBreaker,
    CircuitState,
    generate_litellm_proxy_config,
)


def test_budget_guard_thresholds():
    manager = BudgetGuardManager({
        "backend_engineer": RoleBudget(
            role_id="backend_engineer",
            tokens_per_minute=500_000,
            requests_per_minute=60,
            monthly_budget_cap_usd=100.0,
            current_month_spend_usd=0.0
        )
    })

    # 1. Normal state
    status, util = manager.check_budget_status("backend_engineer")
    assert status == "NORMAL"
    assert util == 0.0

    # 2. Soft alert at 80%
    manager.record_spend("backend_engineer", 82.0)
    status, util = manager.check_budget_status("backend_engineer")
    assert status == "SOFT_ALERT_80"
    assert util == 0.82

    # 3. Critical alert at 95%
    manager.record_spend("backend_engineer", 14.0)  # Total 96.0
    status, util = manager.check_budget_status("backend_engineer")
    assert status == "CRITICAL_ALERT_95"

    # 4. Hard halt at 100%
    manager.record_spend("backend_engineer", 5.0)  # Total 101.0
    status, util = manager.check_budget_status("backend_engineer")
    assert status == "HARD_HALT_100"


def test_circuit_breaker_state_transitions():
    cb = InferenceCircuitBreaker(failure_threshold=3, recovery_timeout_seconds=0.1)

    assert cb.get_state() == CircuitState.CLOSED

    # 1. Record failures up to threshold
    cb.record_failure()
    cb.record_failure()
    assert cb.get_state() == CircuitState.CLOSED

    # 2. Tripping failure -> OPEN
    state, reason = cb.record_failure()
    assert state == CircuitState.OPEN
    assert cb.get_state() == CircuitState.OPEN

    # 3. Wait for cooldown -> HALF_OPEN (Probing)
    import time
    time.sleep(0.15)
    assert cb.get_state() == CircuitState.HALF_OPEN

    # 4. Successful probe -> CLOSED
    cb.record_success()
    assert cb.get_state() == CircuitState.CLOSED


def test_litellm_config_generator(tmp_path):
    out_file = tmp_path / "test_litellm.yaml"
    cfg = generate_litellm_proxy_config("providers.yaml", str(out_file))

    assert "model_list" in cfg
    assert "litellm_settings" in cfg
    assert len(cfg["litellm_settings"]["user_budgets"]) == 13
    assert out_file.exists()
