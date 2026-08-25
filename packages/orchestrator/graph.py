"""Main LangGraph Workflow Definition for DevCorp AI."""
import logging
from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, START, END

from .state import OrgState
from .nodes import (
    product_manager_node,
    router_architect_node,
    requirements_architect_node,
    system_architect_node,
    data_architect_node,
    ux_architect_node,
    security_architect_node,
    engineering_manager_node,
    router_engineer_node,
    specialist_engineers_node,
    qa_reviewer_node,
    demo_release_node,
    standup_review_node,
    delta_replanning_node,
)
from .checkpointer import get_checkpointer

logger = logging.getLogger(__name__)


def decide_qa_verdict(state: OrgState) -> Literal["demo_release", "specialist_engineers"]:
    """Conditional router based on QA review result."""
    if state.get("qa_review_passed", False):
        logger.info("[QA Gate] Quality checks APPROVED -> routing to Demo Synthesis.")
        return "demo_release"
    logger.warning("[QA Gate] Quality checks REJECTED -> routing back to Engineers.")
    return "specialist_engineers"


def decide_standup_feedback(state: OrgState) -> Literal["delta_replanning", "__end__"]:
    """Conditional router based on human executive standup feedback."""
    feedback = state.get("executive_feedback")
    if feedback and feedback.strip():
        logger.info("[Standup Gate] Executive feedback received -> initiating Delta Replanning.")
        return "delta_replanning"
    logger.info("[Standup Gate] No delta feedback -> Sprint finalized successfully.")
    return "__end__"


def create_org_graph(checkpointer: Any = None) -> Any:
    """Build and compile the DevCorp AI multi-agent organizational StateGraph."""
    builder = StateGraph(OrgState)

    # 1. Add All Nodes
    builder.add_node("product_manager", product_manager_node)
    builder.add_node("router_architect", router_architect_node)
    
    # Tier 2 Architects
    builder.add_node("requirements_architect", requirements_architect_node)
    builder.add_node("system_architect", system_architect_node)
    builder.add_node("data_architect", data_architect_node)
    builder.add_node("ux_architect", ux_architect_node)
    builder.add_node("security_architect", security_architect_node)

    # Tier 3 & 4
    builder.add_node("engineering_manager", engineering_manager_node)
    builder.add_node("router_engineer", router_engineer_node)
    builder.add_node("specialist_engineers", specialist_engineers_node)

    # Tier 5 & 6
    builder.add_node("qa_reviewer", qa_reviewer_node)
    builder.add_node("demo_release", demo_release_node)

    # Governance & Replanning
    builder.add_node("standup_review", standup_review_node)
    builder.add_node("delta_replanning", delta_replanning_node)

    # 2. Add Edges
    builder.add_edge(START, "product_manager")
    builder.add_edge("product_manager", "router_architect")

    # Parallel Architect Fan-out
    builder.add_edge("router_architect", "requirements_architect")
    builder.add_edge("router_architect", "system_architect")
    builder.add_edge("router_architect", "data_architect")
    builder.add_edge("router_architect", "ux_architect")
    builder.add_edge("router_architect", "security_architect")

    # Parallel Architect Fan-in
    builder.add_edge("requirements_architect", "engineering_manager")
    builder.add_edge("system_architect", "engineering_manager")
    builder.add_edge("data_architect", "engineering_manager")
    builder.add_edge("ux_architect", "engineering_manager")
    builder.add_edge("security_architect", "engineering_manager")

    # Engineering Dispatch & Execution
    builder.add_edge("engineering_manager", "router_engineer")
    builder.add_edge("router_engineer", "specialist_engineers")
    builder.add_edge("specialist_engineers", "qa_reviewer")

    # QA Conditional Gate
    builder.add_conditional_edges(
        "qa_reviewer",
        decide_qa_verdict,
        {
            "demo_release": "demo_release",
            "specialist_engineers": "specialist_engineers",
        }
    )

    # Demo to Standup
    builder.add_edge("demo_release", "standup_review")

    # Standup Gate Conditional Edge
    builder.add_conditional_edges(
        "standup_review",
        decide_standup_feedback,
        {
            "delta_replanning": "delta_replanning",
            "__end__": END,
        }
    )

    # Delta replanning loops back to PM for new sprint iteration
    builder.add_edge("delta_replanning", "product_manager")

    # 3. Compile with Checkpointer & Interrupts
    if checkpointer is None:
        checkpointer = get_checkpointer(use_postgres=False)

    return builder.compile(
        checkpointer=checkpointer,
        interrupt_before=["standup_review"]
    )
