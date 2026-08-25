"""Unit tests for Dashboard FastAPI Backend Endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from packages.dashboard.api.main import app


@pytest.mark.asyncio
async def test_dashboard_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_dashboard_kanban_and_budgets():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/kanban")
        assert resp.status_code == 200
        assert "columns" in resp.json()

        resp_b = await client.get("/api/budgets/status")
        assert resp_b.status_code == 200
        assert "backend_engineer" in resp_b.json()


@pytest.mark.asyncio
async def test_dashboard_trajectories_and_feedback():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp_t = await client.get("/api/trajectories/backend_engineer")
        assert resp_t.status_code == 200
        assert resp_t.json()["total_steps"] > 0

        resp_f = await client.post(
            "/api/feedback",
            json={"sprint_number": 1, "feedback_text": "Make charts responsive"}
        )
        assert resp_f.status_code == 200
        assert resp_f.json()["status"] == "ACCEPTED"
