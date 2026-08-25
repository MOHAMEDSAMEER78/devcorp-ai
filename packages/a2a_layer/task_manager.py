"""A2A Stateful Task Lifecycle Manager."""
import uuid
import logging
from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class A2ATaskState(str, Enum):
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input-required"
    COMPLETED = "completed"
    FAILED = "failed"


class A2ATask(BaseModel):
    task_id: str = Field(default_factory=lambda: f"task-{uuid.uuid4().hex[:8]}")
    skill_id: str
    target_agent: str
    state: A2ATaskState = Field(default=A2ATaskState.SUBMITTED)
    input_payload: Dict[str, Any] = Field(default_factory=dict)
    output_artifact: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class A2ATaskManager:
    """Manages horizontal collaborative task lifecycles across DSH agents."""

    def __init__(self):
        self.tasks: Dict[str, A2ATask] = {}

    def create_task(self, skill_id: str, target_agent: str, input_payload: Dict[str, Any]) -> A2ATask:
        task = A2ATask(
            skill_id=skill_id,
            target_agent=target_agent,
            input_payload=input_payload,
            state=A2ATaskState.SUBMITTED
        )
        self.tasks[task.task_id] = task
        return task

    def update_state(self, task_id: str, new_state: A2ATaskState, artifact: Optional[Dict[str, Any]] = None, error: Optional[str] = None) -> A2ATask:
        task = self.tasks.get(task_id)
        if not task:
            raise KeyError(f"Task {task_id} not found")
        task.state = new_state
        task.updated_at = datetime.now(timezone.utc).isoformat()
        if artifact is not None:
            task.output_artifact = artifact
        if error is not None:
            task.error_message = error
        return task

    def get_task(self, task_id: str) -> Optional[A2ATask]:
        return self.tasks.get(task_id)
