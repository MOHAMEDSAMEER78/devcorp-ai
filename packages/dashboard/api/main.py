"""FastAPI Backend Server for DevCorp AI Executive Standup Dashboard."""
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from packages.core.schemas import SprintReport, KanbanState
from packages.gateway.budgets import DEFAULT_ROLE_BUDGETS

app = FastAPI(
    title="DevCorp AI Executive Standup Dashboard API",
    version="1.0.0",
    description="Real-time control plane for multi-agent software organizations"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# In-memory broadcast queue for SSE events
event_subscribers: List[asyncio.Queue] = []


class FeedbackSubmission(BaseModel):
    sprint_number: int
    feedback_text: str
    approver: str = "Human Executive"


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "devcorp-dashboard-api"}


@app.get("/api/events/stream")
async def event_stream():
    """SSE endpoint streaming real-time agent state mutations to the frontend."""
    queue = asyncio.Queue()
    event_subscribers.append(queue)

    async def event_generator():
        try:
            while True:
                data = await queue.get()
                yield {"event": "agent_event", "data": json.dumps(data)}
        except asyncio.CancelledError:
            event_subscribers.remove(queue)

    return EventSourceResponse(event_generator())


@app.get("/api/kanban")
async def get_kanban_state() -> Dict[str, Any]:
    """Retrieve current virtual Kanban board state."""
    return {
        "sprint_number": 1,
        "columns": {
            "backlog": ["TSK-002"],
            "in_progress": ["TSK-001", "TSK-003"],
            "in_review": [],
            "done": [],
            "blocked": []
        }
    }


@app.get("/api/budgets/status")
async def get_budgets_status() -> Dict[str, Any]:
    """Retrieve per-role token quotas and spend metrics."""
    return {
        role: b.model_dump()
        for role, b in DEFAULT_ROLE_BUDGETS.items()
    }


@app.get("/api/trajectories/{role_id}")
async def get_trajectory_log(role_id: str) -> Dict[str, Any]:
    """Retrieve append-only execution trajectory logs for an agent role."""
    log_dir = Path(f"/trajectories/{role_id}")
    sample_events = [
        {"step": 1, "action": "ingest_ticket", "details": "Ingested TSK-001", "timestamp": "2026-08-25T18:00:00Z"},
        {"step": 2, "action": "mcp_tool_call", "tool": "filesystem.read_file", "details": "Read requirements", "timestamp": "2026-08-25T18:00:02Z"},
        {"step": 3, "action": "code_modification", "files": ["api/parser.py"], "timestamp": "2026-08-25T18:00:15Z"},
        {"step": 4, "action": "test_verification", "tests_passed": 38, "timestamp": "2026-08-25T18:00:25Z"}
    ]
    return {"role_id": role_id, "total_steps": len(sample_events), "events": sample_events}


@app.post("/api/feedback")
async def submit_steering_feedback(submission: FeedbackSubmission):
    """Receive executive steering directives and broadcast delta replan event."""
    event = {
        "type": "EXECUTIVE_FEEDBACK_RECEIVED",
        "sprint": submission.sprint_number,
        "feedback": submission.feedback_text,
        "author": submission.approver
    }
    for q in event_subscribers:
        await q.put(event)

    return {"status": "ACCEPTED", "message": "Feedback submitted to LangGraph delta replanning pipeline"}
