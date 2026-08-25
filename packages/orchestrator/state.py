"""Organizational State Definition for LangGraph Macro Orchestrator."""
from typing import Dict, Any, List, Optional, TypedDict
from packages.core.schemas import (
    ProductRequirementsDocument,
    RequirementsContract,
    SystemArchitecture,
    DataArchitecture,
    UXSpecification,
    SecuritySpecification,
    TaskDAG,
    KanbanState,
    ArtifactBundle,
    SprintReport,
    TokenUsageMetric,
    DeltaDocument,
)


class OrgState(TypedDict):
    """Global multi-agent organizational state passed across LangGraph nodes."""
    # Input
    executive_concept: str
    
    # Tier 1
    prd: Optional[ProductRequirementsDocument]
    
    # Tier 2 (Architect Pool)
    active_architects: List[str]
    requirements_contract: Optional[RequirementsContract]
    system_architecture: Optional[SystemArchitecture]
    data_architecture: Optional[DataArchitecture]
    ux_specification: Optional[UXSpecification]
    security_specification: Optional[SecuritySpecification]
    
    # Tier 3 (Engineering Management)
    task_dag: Optional[TaskDAG]
    kanban: KanbanState
    
    # Tier 4 (Engineering Execution)
    active_engineers: List[str]
    code_artifacts: Dict[str, Any]
    
    # Tier 5 (Quality Assurance & Review)
    qa_review_passed: bool
    qa_review_verdict: Dict[str, Any]
    qa_retries: Dict[str, int]
    
    # Tier 6 (Demo & Standup)
    current_sprint: int
    demo_bundle: Optional[ArtifactBundle]
    sprint_report: Optional[SprintReport]
    
    # HITL Standup Governance & Delta Replanning
    standup_ready: bool
    executive_feedback: Optional[str]
    delta_document: Optional[DeltaDocument]
    
    # Audit & Resilience
    token_usage: Dict[str, TokenUsageMetric]
    error_logs: List[str]
    trajectory_index: Dict[str, str]
