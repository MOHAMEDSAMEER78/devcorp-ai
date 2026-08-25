"""Security Specification & Threat Model Schema."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ThreatModelEntry(BaseModel):
    threat_id: str = Field(..., description="E.g., T-01")
    stride_category: str = Field(..., description="Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation of Privilege")
    target_component: str = Field(...)
    threat_description: str = Field(...)
    mitigation_strategy: str = Field(...)
    residual_risk: str = Field(default="low", description="low, medium, high")


class AuthFlowSpec(BaseModel):
    auth_type: str = Field(..., description="E.g., OAuth2_OIDC, JWT_Bearer, API_Key")
    token_expiry_seconds: int = Field(default=3600)
    refresh_token_enabled: bool = Field(default=True)
    rbac_roles: List[str] = Field(default_factory=list)


class SecuritySpecification(BaseModel):
    """Security policies and threat models synthesized by Tier 2 Security Architect."""
    version: str = Field(default="1.0.0")
    threat_model: List[ThreatModelEntry] = Field(default_factory=list)
    auth_flow: AuthFlowSpec = Field(...)
    data_encryption: Dict[str, str] = Field(default_factory=dict, description="at_rest, in_transit specs")
    rate_limiting_rules: Dict[str, str] = Field(default_factory=dict)
    owasp_checklist: Dict[str, bool] = Field(default_factory=dict)
