"""Unit and Integration tests for LangGraph Orchestration & Checkpoint Resumption."""
import pytest
from packages.orchestrator import (
    create_org_graph,
    SwarmCircuitBreaker,
    get_checkpointer,
)
from packages.orchestrator.state import OrgState


@pytest.mark.asyncio
async def test_full_graph_execution_to_standup_interrupt():
    """Test full pipeline execution from concept to HITL standup interrupt."""
    checkpointer = get_checkpointer(use_postgres=False)
    graph = create_org_graph(checkpointer=checkpointer)

    thread_config = {"configurable": {"thread_id": "test-sprint-1"}}

    initial_state: OrgState = {
        "executive_concept": "Build a personal bank statement expense tracking web application",
        "prd": None,
        "active_architects": [],
        "requirements_contract": None,
        "system_architecture": None,
        "data_architecture": None,
        "ux_specification": None,
        "security_specification": None,
        "task_dag": None,
        "kanban": {"sprint_number": 1, "columns": {}, "total_tickets": 0, "completed_tickets": 0},
        "active_engineers": [],
        "code_artifacts": {},
        "qa_review_passed": False,
        "qa_review_verdict": {},
        "qa_retries": {},
        "current_sprint": 1,
        "demo_bundle": None,
        "sprint_report": None,
        "standup_ready": False,
        "executive_feedback": None,
        "delta_document": None,
        "token_usage": {},
        "error_logs": [],
        "trajectory_index": {},
    }

    # Execute graph - it will run until the interrupt_before=["standup_review"]
    result = await graph.ainvoke(initial_state, config=thread_config)

    # 1. Assert PRD generated
    assert result["prd"] is not None
    assert "Bank Statement" in result["prd"].title

    # 2. Assert Architect Pool executed
    assert len(result["active_architects"]) == 5
    assert result["requirements_contract"] is not None
    assert result["system_architecture"] is not None
    assert result["data_architecture"] is not None
    assert result["ux_specification"] is not None
    assert result["security_specification"] is not None

    # 3. Assert Engineering Management & WBS generated
    assert result["task_dag"] is not None
    assert len(result["task_dag"].tickets) == 3
    assert len(result["active_engineers"]) == 3

    # 4. Assert Real Code was generated and verified by QA
    assert result["code_artifacts"]["status"] == "GENERATED"
    assert len(result["code_artifacts"]["files_modified"]) >= 4
    assert result["qa_review_passed"] is True
    assert result["demo_bundle"] is not None
    assert result["sprint_report"] is not None
    assert result["sprint_report"].total_tests_passed == 4

    # 5. Check graph state is paused at standup_review
    state_snap = await graph.aget_state(thread_config)
    assert "standup_review" in state_snap.next


@pytest.mark.asyncio
async def test_standup_feedback_and_delta_replanning():
    """Test resuming from checkpoint with executive steering feedback."""
    checkpointer = get_checkpointer(use_postgres=False)
    graph = create_org_graph(checkpointer=checkpointer)
    thread_config = {"configurable": {"thread_id": "test-sprint-replan"}}

    initial_state: OrgState = {
        "executive_concept": "Build expense tracker",
        "prd": None,
        "active_architects": [],
        "requirements_contract": None,
        "system_architecture": None,
        "data_architecture": None,
        "ux_specification": None,
        "security_specification": None,
        "task_dag": None,
        "kanban": {"sprint_number": 1, "columns": {}, "total_tickets": 0, "completed_tickets": 0},
        "active_engineers": [],
        "code_artifacts": {},
        "qa_review_passed": False,
        "qa_review_verdict": {},
        "qa_retries": {},
        "current_sprint": 1,
        "demo_bundle": None,
        "sprint_report": None,
        "standup_ready": False,
        "executive_feedback": None,
        "delta_document": None,
        "token_usage": {},
        "error_logs": [],
        "trajectory_index": {},
    }

    # Run until standup interrupt
    await graph.ainvoke(initial_state, config=thread_config)

    # Executive reviews demo and injects steering feedback
    await graph.aupdate_state(
        thread_config,
        {"executive_feedback": "Add collapsible sidebar and category budget progress bars"}
    )

    # Resume execution -> Delta replanning triggers -> Loops to PM for Sprint 2
    resumed_result = await graph.ainvoke(None, config=thread_config)

    # Assert sprint number advanced and delta document recorded
    assert resumed_result["current_sprint"] == 2
    assert resumed_result["delta_document"] is not None
    assert "collapsible sidebar" in resumed_result["delta_document"].executive_feedback_raw


def test_circuit_breaker():
    """Test retry threshold and syntax oscillation detection."""
    cb = SwarmCircuitBreaker(max_retries_per_ticket=5)

    # Normal retry within limit
    tripped, reason = cb.check_ticket_retry("TSK-101", 3)
    assert tripped is False

    # Max retries breached
    tripped, reason = cb.check_ticket_retry("TSK-101", 5)
    assert tripped is True
    assert "maximum retry limit" in reason

    # Oscillation detection
    diff_a = "+ def parse(): pass"
    diff_b = "- def parse(): pass"

    assert cb.record_and_check_oscillation("TSK-101", diff_a)[0] is False
    assert cb.record_and_check_oscillation("TSK-101", diff_b)[0] is False
    # Re-introducing diff_a within 3 turns triggers oscillation guard
    tripped_osc, osc_reason = cb.record_and_check_oscillation("TSK-101", diff_a)
    assert tripped_osc is True
    assert "oscillation detected" in osc_reason
