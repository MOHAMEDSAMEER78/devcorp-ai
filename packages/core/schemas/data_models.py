"""Data Architecture & Database Schema."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ColumnDefinition(BaseModel):
    name: str = Field(...)
    data_type: str = Field(..., description="E.g., UUID, VARCHAR(255), NUMERIC(12,2), TIMESTAMP")
    primary_key: bool = Field(default=False)
    nullable: bool = Field(default=False)
    unique: bool = Field(default=False)
    foreign_key: Optional[str] = Field(default=None, description="E.g., users.id")
    default_value: Optional[str] = Field(default=None)


class TableDefinition(BaseModel):
    table_name: str = Field(...)
    columns: List[ColumnDefinition] = Field(default_factory=list)
    indexes: List[str] = Field(default_factory=list)
    description: str = Field(...)


class MigrationStep(BaseModel):
    step_number: int = Field(...)
    name: str = Field(..., description="E.g., 001_create_users_and_statements")
    sql_up: str = Field(..., description="DDL statement to apply")
    sql_down: str = Field(..., description="DDL statement to rollback")


class DataArchitecture(BaseModel):
    """Database schemas and migrations synthesized by Tier 2 Data Architect."""
    version: str = Field(default="1.0.0")
    database_type: str = Field(default="PostgreSQL", description="Database engine")
    tables: List[TableDefinition] = Field(default_factory=list)
    er_diagram_mermaid: str = Field(default="", description="Mermaid ER diagram")
    migrations: List[MigrationStep] = Field(default_factory=list)
    caching_strategy: Dict[str, Any] = Field(default_factory=dict)
    validation_schemas: Dict[str, Any] = Field(default_factory=dict)
