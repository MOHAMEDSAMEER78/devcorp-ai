"""System Architecture Schema."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ServiceComponent(BaseModel):
    id: str = Field(..., description="Unique component ID, e.g., api_gateway, auth_service")
    name: str = Field(..., description="Human-readable component name")
    technology: str = Field(..., description="E.g., FastAPI, React, Redis, PostgreSQL")
    port: Optional[int] = Field(default=None)
    dependencies: List[str] = Field(default_factory=list, description="IDs of components this relies on")
    description: str = Field(...)


class APIEndpointSpec(BaseModel):
    path: str = Field(..., description="E.g., /api/v1/statements/upload")
    method: str = Field(..., description="GET, POST, PUT, DELETE, PATCH")
    summary: str = Field(...)
    request_schema_ref: Optional[str] = Field(default=None)
    response_schema_ref: Optional[str] = Field(default=None)
    auth_required: bool = Field(default=True)


class SystemArchitecture(BaseModel):
    """System topology and API contracts synthesized by Tier 2 System Architect."""
    version: str = Field(default="1.0.0")
    tech_stack: Dict[str, str] = Field(..., description="Mapping: frontend, backend, database, cache, runtime")
    components: List[ServiceComponent] = Field(default_factory=list)
    endpoints: List[APIEndpointSpec] = Field(default_factory=list)
    openapi_spec: Dict[str, Any] = Field(default_factory=dict, description="OpenAPI 3.1 JSON definition")
    sequence_diagrams: Dict[str, str] = Field(default_factory=dict, description="Mermaid diagrams per user journey")
    deployment_topology: Dict[str, Any] = Field(default_factory=dict)
