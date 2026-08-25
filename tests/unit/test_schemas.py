"""Unit tests for DevCorp AI Pydantic Schemas."""
import pytest
from pydantic import ValidationError
from packages.core.schemas import (
    ProductRequirementsDocument,
    UserStory,
    AcceptanceCriterion,
    RequirementsContract,
    PerformanceSLA,
    SystemArchitecture,
    ServiceComponent,
    DataArchitecture,
    TableDefinition,
    ColumnDefinition,
    UXSpecification,
    PageWireframe,
    UIComponentNode,
    SecuritySpecification,
    ThreatModelEntry,
    AuthFlowSpec,
    TaskTicket,
    TaskDAG,
    KanbanState,
    TicketStatus,
    ArtifactBundle,
    SprintReport,
    TokenUsageMetric,
    DeltaDocument,
)


def test_prd_validation():
    prd = ProductRequirementsDocument(
        title="Bank Statement Expense Tracker",
        executive_summary="Autonomous personal expense tracking platform",
        user_stories=[
            UserStory(
                id="US-01",
                title="Upload Statement",
                as_a="User",
                i_want="to upload my PDF bank statement",
                so_that="transactions are automatically extracted",
                acceptance_criteria=[
                    AcceptanceCriterion(
                        id="AC-01",
                        given="A valid PDF statement file",
                        when="User submits the upload form",
                        then="Statement status changes to PROCESSING"
                    )
                ]
            )
        ]
    )
    assert prd.title == "Bank Statement Expense Tracker"
    assert len(prd.user_stories) == 1
    assert prd.user_stories[0].acceptance_criteria[0].id == "AC-01"


def test_contracts_validation():
    contract = RequirementsContract(
        prd_version="1.0.0",
        performance_slas=[
            PerformanceSLA(metric="p95_parse_latency_ms", target=500.0, unit="ms")
        ],
        edge_cases=[]
    )
    assert contract.performance_slas[0].target == 500.0


def test_architecture_validation():
    arch = SystemArchitecture(
        tech_stack={"frontend": "React", "backend": "FastAPI", "db": "PostgreSQL"},
        components=[
            ServiceComponent(
                id="backend_api",
                name="FastAPI Backend",
                technology="FastAPI",
                port=8000,
                description="Core REST API"
            )
        ]
    )
    assert arch.components[0].port == 8000


def test_data_architecture_validation():
    data_arch = DataArchitecture(
        database_type="PostgreSQL",
        tables=[
            TableDefinition(
                table_name="transactions",
                columns=[
                    ColumnDefinition(name="id", data_type="UUID", primary_key=True),
                    ColumnDefinition(name="amount", data_type="NUMERIC(12,2)")
                ],
                description="Bank transaction records"
            )
        ]
    )
    assert len(data_arch.tables[0].columns) == 2


def test_ux_specification_validation():
    ux = UXSpecification(
        pages=[
            PageWireframe(
                page_id="dashboard",
                route="/dashboard",
                title="Expense Dashboard",
                layout_tree=UIComponentNode(
                    id="root",
                    type="Container",
                    label="Main View"
                )
            )
        ]
    )
    assert ux.pages[0].route == "/dashboard"


def test_security_specification_validation():
    sec = SecuritySpecification(
        threat_model=[
            ThreatModelEntry(
                threat_id="T-01",
                stride_category="Tampering",
                target_component="file_upload",
                threat_description="Malicious PDF payload upload",
                mitigation_strategy="Sanitize via PDF parser in isolated sandbox"
            )
        ],
        auth_flow=AuthFlowSpec(auth_type="OAuth2_OIDC")
    )
    assert sec.auth_flow.auth_type == "OAuth2_OIDC"


def test_task_ticket_validation():
    ticket = TaskTicket(
        ticket_id="TSK-01",
        title="Build Statement Parser",
        description="Extract transactions from PDF",
        domain_tags=["api", "scraping"],
        assigned_role="engineer-backend",
        status=TicketStatus.IN_PROGRESS
    )
    assert "scraping" in ticket.domain_tags
    assert ticket.status == TicketStatus.IN_PROGRESS


def test_artifact_bundle_and_sprint_report():
    report = SprintReport(
        sprint_number=1,
        completed_user_stories=["US-01", "US-02"],
        test_coverage_percent=94.5,
        total_tests_passed=24,
        total_tests_failed=0,
        token_metrics=[
            TokenUsageMetric(
                role_id="engineer-backend",
                input_tokens=15000,
                output_tokens=4200,
                total_cost_usd=0.045
            )
        ]
    )
    assert report.sprint_number == 1
    assert report.test_coverage_percent == 94.5
