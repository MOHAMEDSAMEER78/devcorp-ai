"""Granular Per-Role Token Quotas and Budget Guards for 13 Specialist Roles."""
from typing import Dict, Any, Tuple
from pydantic import BaseModel, Field


class RoleBudget(BaseModel):
    role_id: str
    tokens_per_minute: int
    requests_per_minute: int
    monthly_budget_cap_usd: float
    current_month_spend_usd: float = Field(default=0.0)


# Standard Budget Table across the 13-agent organization (~$815 total monthly ceiling)
DEFAULT_ROLE_BUDGETS: Dict[str, RoleBudget] = {
    "product_manager": RoleBudget(
        role_id="product_manager",
        tokens_per_minute=200_000,
        requests_per_minute=30,
        monthly_budget_cap_usd=50.0,
    ),
    "requirements_architect": RoleBudget(
        role_id="requirements_architect",
        tokens_per_minute=150_000,
        requests_per_minute=25,
        monthly_budget_cap_usd=40.0,
    ),
    "system_architect": RoleBudget(
        role_id="system_architect",
        tokens_per_minute=200_000,
        requests_per_minute=30,
        monthly_budget_cap_usd=50.0,
    ),
    "data_architect": RoleBudget(
        role_id="data_architect",
        tokens_per_minute=150_000,
        requests_per_minute=25,
        monthly_budget_cap_usd=40.0,
    ),
    "ux_architect": RoleBudget(
        role_id="ux_architect",
        tokens_per_minute=150_000,
        requests_per_minute=25,
        monthly_budget_cap_usd=40.0,
    ),
    "security_architect": RoleBudget(
        role_id="security_architect",
        tokens_per_minute=100_000,
        requests_per_minute=20,
        monthly_budget_cap_usd=30.0,
    ),
    "agent_router": RoleBudget(
        role_id="agent_router",
        tokens_per_minute=50_000,
        requests_per_minute=60,
        monthly_budget_cap_usd=15.0,
    ),
    "engineering_manager": RoleBudget(
        role_id="engineering_manager",
        tokens_per_minute=100_000,
        requests_per_minute=20,
        monthly_budget_cap_usd=30.0,
    ),
    "backend_engineer": RoleBudget(
        role_id="backend_engineer",
        tokens_per_minute=500_000,
        requests_per_minute=60,
        monthly_budget_cap_usd=200.0,
    ),
    "frontend_engineer": RoleBudget(
        role_id="frontend_engineer",
        tokens_per_minute=400_000,
        requests_per_minute=50,
        monthly_budget_cap_usd=150.0,
    ),
    "ux_engineer": RoleBudget(
        role_id="ux_engineer",
        tokens_per_minute=200_000,
        requests_per_minute=30,
        monthly_budget_cap_usd=60.0,
    ),
    "qa_reviewer": RoleBudget(
        role_id="qa_reviewer",
        tokens_per_minute=300_000,
        requests_per_minute=40,
        monthly_budget_cap_usd=80.0,
    ),
    "demo_release": RoleBudget(
        role_id="demo_release",
        tokens_per_minute=100_000,
        requests_per_minute=20,
        monthly_budget_cap_usd=30.0,
    ),
}


class BudgetGuardManager:
    """Manages role spend tracking, soft alert thresholds, and hard halt enforcement."""

    def __init__(self, budgets: Dict[str, RoleBudget] | None = None):
        self.budgets = budgets or DEFAULT_ROLE_BUDGETS.copy()

    def record_spend(self, role_id: str, cost_usd: float) -> None:
        if role_id in self.budgets:
            self.budgets[role_id].current_month_spend_usd += cost_usd

    def check_budget_status(self, role_id: str) -> Tuple[str, float]:
        """Check budget status for a role.
        
        Returns:
            (status: 'NORMAL' | 'SOFT_ALERT_80' | 'CRITICAL_ALERT_95' | 'HARD_HALT_100', utilization_ratio: float)
        """
        budget = self.budgets.get(role_id)
        if not budget or budget.monthly_budget_cap_usd <= 0:
            return "NORMAL", 0.0

        utilization = budget.current_month_spend_usd / budget.monthly_budget_cap_usd

        if utilization >= 1.0:
            return "HARD_HALT_100", utilization
        if utilization >= 0.95:
            return "CRITICAL_ALERT_95", utilization
        if utilization >= 0.80:
            return "SOFT_ALERT_80", utilization
        return "NORMAL", utilization
