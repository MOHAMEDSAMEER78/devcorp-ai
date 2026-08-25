"""Artifact Bundle, Sprint Report, and Delta Document Schemas."""
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class ArtifactItem(BaseModel):
    name: str = Field(...)
    artifact_type: str = Field(..., description="code_diff, test_log, mp4_video, playwright_trace, json_schema")
    uri_or_path: str = Field(...)
    sha256: Optional[str] = Field(default=None)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ArtifactBundle(BaseModel):
    """Deliverable bundle packaged by Demo Agent or Engineering Agents."""
    bundle_id: str = Field(...)
    sprint_id: str = Field(...)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    items: List[ArtifactItem] = Field(default_factory=list)
    manifest: Dict[str, Any] = Field(default_factory=dict)


class TokenUsageMetric(BaseModel):
    role_id: str = Field(...)
    input_tokens: int = Field(default=0)
    output_tokens: int = Field(default=0)
    total_cost_usd: float = Field(default=0.0)
    budget_cap_usd: float = Field(default=0.0)
    budget_utilized_percent: float = Field(default=0.0)


class SprintReport(BaseModel):
    """Executive sprint summary rendered on Standup Dashboard and sent to Meet/Teams bots."""
    sprint_number: int = Field(...)
    completed_user_stories: List[str] = Field(default_factory=list)
    test_coverage_percent: float = Field(default=0.0)
    total_tests_passed: int = Field(default=0)
    total_tests_failed: int = Field(default=0)
    token_metrics: List[TokenUsageMetric] = Field(default_factory=list)
    total_sprint_cost_usd: float = Field(default=0.0)
    demo_video_url: Optional[str] = Field(default=None)
    interactive_sandbox_url: Optional[str] = Field(default=None)
    trajectory_log_path: Optional[str] = Field(default=None)
    blockers_or_escalations: List[str] = Field(default_factory=list)


class DeltaDocument(BaseModel):
    """Semantic diff of requirements produced by PM following executive standup feedback."""
    delta_id: str = Field(...)
    sprint_number: int = Field(...)
    executive_feedback_raw: str = Field(...)
    modified_user_stories: List[Dict[str, Any]] = Field(default_factory=list)
    added_user_stories: List[Dict[str, Any]] = Field(default_factory=list)
    removed_user_stories: List[str] = Field(default_factory=list)
    impacted_architects: List[str] = Field(default_factory=list, description="List of architect IDs needing delta updates")
