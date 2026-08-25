"""Unit tests for Operational Guardrails."""
from packages.orchestrator.guardrails import SwarmGuardrailManager
from packages.core.schemas import TaskTicket, TicketStatus


def test_guardrail_schema_validation():
    mgr = SwarmGuardrailManager()
    valid, err = mgr.validate_schema_compliance(
        {
            "ticket_id": "TSK-01",
            "title": "Build Parser",
            "description": "Parser detail",
            "status": "in_progress"
        },
        TaskTicket
    )
    assert valid is True
    assert err is None


def test_guardrail_sandbox_escape_prevention():
    mgr = SwarmGuardrailManager()
    
    # Safe command
    safe, err = mgr.verify_no_sandbox_escape("pytest tests/ -v")
    assert safe is True

    # Dangerous destructive command
    safe, err = mgr.verify_no_sandbox_escape("rm -rf / --no-preserve-root")
    assert safe is False
    assert "rejected" in err
