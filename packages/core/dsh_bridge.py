"""DSH Bridge: Interface between LangGraph (Python) and DeepSeek Harness (dsh) Agent Instances."""
from typing import Dict, Any, Optional, Type, TypeVar
import json
import logging
import httpx
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)
logger = logging.getLogger(__name__)


class DSHAgentClient:
    """HTTP / A2A Client communicating with a running DeepSeek Harness instance."""

    def __init__(self, base_url: str, timeout_seconds: float = 300.0):
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    async def get_agent_card(self) -> Dict[str, Any]:
        """Fetch the A2A Agent Card from the DSH instance."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{self.base_url}/.well-known/agent.json")
            resp.raise_for_status()
            return resp.json()

    async def dispatch_task(
        self,
        skill_id: str,
        payload: Dict[str, Any],
        expected_schema: Optional[Type[T]] = None,
    ) -> T | Dict[str, Any]:
        """Dispatch a stateful task to the DSH agent and wait for artifact completion."""
        request_body = {
            "jsonrpc": "2.0",
            "method": "tasks/create",
            "params": {
                "skill": skill_id,
                "input": payload,
            },
            "id": "task-001"
        }

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            logger.info(f"Dispatching task '{skill_id}' to DSH agent at {self.base_url}")
            resp = await client.post(
                f"{self.base_url}/a2a/tasks",
                json=request_body,
                headers={"Content-Type": "application/json"}
            )
            resp.raise_for_status()
            data = resp.json()

        result_payload = data.get("result", {}).get("artifact", data.get("result", {}))

        if expected_schema:
            if isinstance(result_payload, str):
                result_payload = json.loads(result_payload)
            return expected_schema.model_validate(result_payload)

        return result_payload


class DSHBridge:
    """Central registry and dispatcher for all 13 DSH specialist agent instances."""

    def __init__(self, agent_endpoints: Optional[Dict[str, str]] = None):
        # Default local development port mapping
        self.agent_endpoints = agent_endpoints or {
            "product_manager": "http://localhost:8081",
            "requirements_architect": "http://localhost:8082",
            "system_architect": "http://localhost:8083",
            "data_architect": "http://localhost:8084",
            "ux_architect": "http://localhost:8085",
            "security_architect": "http://localhost:8086",
            "agent_router": "http://localhost:8087",
            "engineering_manager": "http://localhost:8088",
            "backend_engineer": "http://localhost:8089",
            "frontend_engineer": "http://localhost:8090",
            "ux_engineer": "http://localhost:8091",
            "qa_reviewer": "http://localhost:8092",
            "demo_release": "http://localhost:8093",
        }

    def get_client(self, role_id: str) -> DSHAgentClient:
        endpoint = self.agent_endpoints.get(role_id)
        if not endpoint:
            raise KeyError(f"No DSH endpoint registered for agent role '{role_id}'")
        return DSHAgentClient(base_url=endpoint)
