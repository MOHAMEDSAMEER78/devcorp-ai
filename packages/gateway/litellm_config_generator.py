"""LiteLLM Configuration Generator and Runtime Syncer."""
import yaml
from pathlib import Path
from typing import Dict, Any
from packages.core.provider_registry import ProviderRegistry
from .budgets import DEFAULT_ROLE_BUDGETS


def generate_litellm_proxy_config(
    providers_yaml_path: str = "providers.yaml",
    output_path: str = "litellm_config.yaml"
) -> Dict[str, Any]:
    """Compile providers registry and role budgets into LiteLLM proxy configuration."""
    registry = ProviderRegistry.from_yaml(providers_yaml_path)
    config_dict = registry.to_litellm_config()

    # Inject per-role user budget allocations into LiteLLM settings
    user_budgets = []
    for role_id, b in DEFAULT_ROLE_BUDGETS.items():
        user_budgets.append({
            "user_id": f"role_{role_id}",
            "max_budget": b.monthly_budget_cap_usd,
            "budget_duration": "monthly",
            "tpm_limit": b.tokens_per_minute,
            "rpm_limit": b.requests_per_minute,
        })

    config_dict["litellm_settings"] = {
        "user_budgets": user_budgets,
        "alert_on_max_budget": True,
        "set_verbose": False,
    }

    # Write out YAML configuration file
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)

    return config_dict
