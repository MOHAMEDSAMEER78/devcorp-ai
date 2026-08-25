"""Scalable LLM Provider Registry and LiteLLM Configuration Generator."""
from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml
from pydantic import BaseModel, Field


class ProviderConfig(BaseModel):
    """Configuration for an individual Foundation Model provider."""
    name: str = Field(..., description="Unique provider identifier, e.g., gemini-pro, local-qwen")
    model_id: str = Field(..., description="LiteLLM model string, e.g., gemini/gemini-2.5-pro")
    endpoint: Optional[str] = Field(default=None, description="API Base URL if custom/local")
    auth_type: str = Field(default="api_key", description="api_key, bearer, none")
    auth_env_var: Optional[str] = Field(default=None, description="Environment variable holding the secret")
    tier: str = Field(..., description="primary, secondary, local, tertiary")
    capabilities: List[str] = Field(default_factory=list, description="reasoning, coding, multimodal")
    enabled: bool = Field(default=True, description="Toggle provider availability")
    max_context_tokens: int = Field(default=128000)
    cost_per_1k_input: float = Field(default=0.0)
    cost_per_1k_output: float = Field(default=0.0)


class ProviderRegistry(BaseModel):
    """Registry managing dynamic LLM provider discovery and LiteLLM export."""
    providers: List[ProviderConfig] = Field(default_factory=list)

    @classmethod
    def from_yaml(cls, path: Path | str) -> "ProviderRegistry":
        """Load providers from a YAML configuration file."""
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Provider configuration not found at {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def get_enabled(self) -> List[ProviderConfig]:
        """Return all active providers."""
        return [p for p in self.providers if p.enabled]

    def get_by_tier(self, tier: str) -> List[ProviderConfig]:
        """Filter enabled providers by priority tier."""
        return [p for p in self.get_enabled() if p.tier == tier]

    def get_by_capability(self, capability: str) -> List[ProviderConfig]:
        """Filter enabled providers by functional capability."""
        return [p for p in self.get_enabled() if capability in p.capabilities]

    def to_litellm_config(self) -> Dict[str, Any]:
        """Generate a complete LiteLLM Proxy configuration dictionary."""
        model_list = []
        for p in self.get_enabled():
            params: Dict[str, Any] = {"model": p.model_id}
            if p.endpoint:
                params["api_base"] = p.endpoint
            if p.auth_env_var:
                params["api_key"] = f"os.environ/{p.auth_env_var}"

            model_list.append({
                "model_name": f"{p.tier}/{p.capabilities[0] if p.capabilities else 'general'}",
                "litellm_params": params,
                "model_info": {
                    "tier": p.tier,
                    "max_tokens": p.max_context_tokens,
                    "input_cost_per_token": p.cost_per_1k_input / 1000.0,
                    "output_cost_per_token": p.cost_per_1k_output / 1000.0,
                }
            })

        # Dynamic fallback chains
        primary_models = [p.model_id for p in self.get_by_tier("primary")]
        secondary_models = [p.model_id for p in self.get_by_tier("secondary")]
        local_models = [p.model_id for p in self.get_by_tier("local")]

        fallbacks = []
        fallback_targets = secondary_models + local_models
        for prim in primary_models:
            if fallback_targets:
                fallbacks.append({prim: fallback_targets})

        return {
            "model_list": model_list,
            "router_settings": {
                "routing_strategy": "usage-based-routing-v2",
                "num_retries": 3,
                "retry_after": 5,
                "allowed_fails": 5,
                "cooldown_time": 60,
                "fallbacks": fallbacks,
            },
            "general_settings": {
                "database_url": "os.environ/LITELLM_DB_URL",
                "master_key": "os.environ/LITELLM_MASTER_KEY",
            }
        }
