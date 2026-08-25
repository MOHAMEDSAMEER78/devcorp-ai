"""Unit tests for A2A Layer Registry and Task Manager."""
import pytest
from packages.a2a_layer import (
    A2ARegistry,
    AgentCard,
    AgentSkill,
    A2ATaskManager,
    A2ATaskState,
)


def test_a2a_registry():
    registry = A2ARegistry()
    card = registry.register_card(
        "backend-engineer",
        {
            "name": "backend-engineer",
            "description": "Backend implementation agent",
            "url": "http://localhost:8089",
            "skills": [
                {"id": "implement-backend-ticket", "name": "Backend Implementation"}
            ]
        }
    )
    assert card.name == "backend-engineer"
    assert len(registry.list_all()) == 1

    matched = registry.find_agents_by_skill("implement-backend-ticket")
    assert len(matched) == 1
    assert matched[0].name == "backend-engineer"


def test_a2a_task_lifecycle():
    manager = A2ATaskManager()
    task = manager.create_task(
        skill_id="implement-backend-ticket",
        target_agent="backend-engineer",
        input_payload={"ticket_id": "TSK-101"}
    )
    assert task.state == A2ATaskState.SUBMITTED

    manager.update_state(task.task_id, A2ATaskState.WORKING)
    assert manager.get_task(task.task_id).state == A2ATaskState.WORKING

    manager.update_state(
        task.task_id,
        A2ATaskState.COMPLETED,
        artifact={"status": "SUCCESS", "diff": "+ def run(): pass"}
    )
    completed_task = manager.get_task(task.task_id)
    assert completed_task.state == A2ATaskState.COMPLETED
    assert completed_task.output_artifact["status"] == "SUCCESS"
