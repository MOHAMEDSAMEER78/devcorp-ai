"""Requirements Contract Schema."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class PerformanceSLA(BaseModel):
    metric: str = Field(..., description="E.g., p95_latency_ms, throughput_rps, max_memory_mb")
    target: float = Field(..., description="Target threshold")
    unit: str = Field(..., description="Unit of measurement: ms, rps, MB")


class EdgeCaseSpecification(BaseModel):
    id: str = Field(..., description="Edge case ID, e.g., EC-01")
    scenario: str = Field(..., description="Specific edge case condition or anomaly")
    handling_strategy: str = Field(..., description="Prescribed behavior or fallback")
    test_assertion: str = Field(..., description="Deterministic verification check")


class RequirementsContract(BaseModel):
    """Formal testable contract synthesized by Tier 2 Requirements Architect."""
    version: str = Field(default="1.0.0")
    prd_version: str = Field(..., description="Referenced PRD version")
    formal_specifications: Dict[str, Any] = Field(default_factory=dict)
    performance_slas: List[PerformanceSLA] = Field(default_factory=list)
    edge_cases: List[EdgeCaseSpecification] = Field(default_factory=list)
    boundary_conditions: Dict[str, str] = Field(default_factory=dict)
    compliance_matrix: Dict[str, bool] = Field(default_factory=dict)
