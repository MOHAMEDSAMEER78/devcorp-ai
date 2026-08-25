"""UX Specification & Wireframe Schema."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class UIComponentNode(BaseModel):
    id: str = Field(..., description="E.g., upload_zone, transaction_table, expense_pie_chart")
    type: str = Field(..., description="E.g., Container, Form, Button, Table, Chart, Modal")
    label: str = Field(...)
    props: Dict[str, Any] = Field(default_factory=dict)
    children: List["UIComponentNode"] = Field(default_factory=list)


class PageWireframe(BaseModel):
    page_id: str = Field(..., description="E.g., login_page, statement_upload, dashboard")
    route: str = Field(..., description="E.g., /dashboard")
    title: str = Field(...)
    layout_tree: UIComponentNode = Field(...)
    responsive_rules: Dict[str, Any] = Field(default_factory=dict)


class DesignTokens(BaseModel):
    color_palette: Dict[str, str] = Field(default_factory=dict)
    typography: Dict[str, Any] = Field(default_factory=dict)
    spacing: Dict[str, str] = Field(default_factory=dict)
    breakpoints: Dict[str, str] = Field(default_factory=dict)


class UXSpecification(BaseModel):
    """UX information architecture and design tokens synthesized by Tier 2 UX Architect."""
    version: str = Field(default="1.0.0")
    design_tokens: DesignTokens = Field(default_factory=DesignTokens)
    pages: List[PageWireframe] = Field(default_factory=list)
    accessibility_guidelines: List[str] = Field(default_factory=list)
    interaction_flows: Dict[str, str] = Field(default_factory=dict, description="Mermaid flowchart of UI transitions")
