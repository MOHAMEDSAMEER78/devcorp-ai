# DevCorp AI — Project Work Log & Changelog

All development sessions, architectural decisions, modifications, and milestones are recorded in this ledger.

---

## [2026-08-25] Project Initialization & Architecture Blueprinting

### Overview
- Established the foundational architecture and detailed 8-phase implementation roadmap for **DevCorp AI** (`devcorp-ai`).
- Initialized dedicated Git repository at `/home/ubuntu/Documents/projects/devcorp-ai` on branch `main`.

### Key Architectural Decisions & Iterations
1. **Hierarchical Topology & Role Expansion (v1 → v2)**:
   - Expanded from 6 generic roles to **13 specialized agents**:
     - *Tier 1*: Product Manager
     - *Tier 2 (Architects)*: Requirements Architect, System Architect, Data Architect, UX Architect, Security Architect
     - *Tier 2/3*: Agent Router (dynamic domain-tag ticket dispatch)
     - *Tier 3*: Engineering Manager
     - *Tier 4 (Engineers)*: Backend Engineer, Frontend/UI Engineer, UX Engineer
     - *Tier 5*: QA / Reviewer
     - *Tier 6*: Demo / Release Agent
2. **DeepSeek Harness (`dsh`) Micro-Kernel Runtime (v2 → v2.1)**:
   - Selected DeepSeek Harness (`dsh`) powered by the Cordis meta-framework as the universal micro-kernel execution runtime for all 13 agents.
   - Converted agent definitions from repetitive Python classes to declarative YAML plugin profiles (`cordis.yml`) and markdown system prompts in `profiles/` and `prompts/`.
   - Utilized `dsh-mcp` for declarative Model Context Protocol tool connections.
   - Utilized `dsh-a2a` for out-of-the-box Agent-to-Agent protocol compliance (JSON Agent Cards, task lifecycle states).
   - Integrated DSH's append-only trajectory subsystem (`.jsonl`) for granular reasoning replays and auditing.
3. **Macro Orchestration (LangGraph)**:
   - Retained LangGraph in Python for organizational state machine management, PostgreSQL thread checkpointing, budget guard enforcement, and Human-in-the-Loop (HITL) interrupt gates.
   - Designed lightweight `dsh_bridge.py` for Python ↔ DSH A2A communication.
4. **Token Resilience & Scalable Provider System**:
   - Centralized LiteLLM Gateway with `providers.yaml` registry allowing zero-code LLM additions.
   - Configurable multi-tier cascading fallback: Primary Cloud → Burst Cloud → Local vLLM (optional) → Tertiary Cloud.
   - Redis-backed 3-state circuit breaker (CLOSED / OPEN / HALF-OPEN).
   - Per-role token quotas and hard budget halts across all 13 roles.
5. **Human-on-the-Loop Governance**:
   - Production React Standup Dashboard with OAuth2/OIDC (Google/GitHub SSO) and real-time Agent Trajectory Explorer.
   - Automated video standup bots for **Google Meet** and **Microsoft Teams**.
   - Playwright automated demo synthesis engine (MP4 video capture with visible cursor overlays).
6. **Dual Deployment Infrastructure**:
   - Docker Compose for local development.
   - Kubernetes Helm charts with Horizontal Pod Autoscaling (HPA) for production.
7. **Reference Testbed Application**:
   - Personal Expense Tracking Web App with Bank Statement Scraping (PDF & CSV parsing, auto-categorization, spending dashboards).

### Repository Artifacts Created
- `docs/architecture_reference.md`: Canonical Reference Architecture v2.1.
- `docs/implementation_plan.md`: Master 8-Phase Implementation Plan v2.1.
- `docs/deepseek_harness_comparison.md`: Detailed DSH vs traditional agent architectures comparison.
- `README.md`: Repository overview, structure, and agent summary.
- `.gitignore`: Ignore rules for Python, Node/DSH, Docker, secrets, and trajectory data.
- `WORKLOG.md`: Continuous project ledger.

---

## [2026-08-25] Phase 0 — Scaffolding & Core Infrastructure Implementation

### Objectives Achieved
1. **Monorepo Scaffolding**:
   - `pyproject.toml` (modern Python 3.12 workspace with Pydantic, LangGraph, LiteLLM, Redis, FastAPI, Playwright, Pytest).
   - `package.json` for managing DeepSeek Harness runtime and Cordis dependencies.
   - `Makefile` with standard developer commands (`setup`, `lint`, `test`, `dev-up`, `dev-down`, `clean`).
   - `.env.example` and `docker-compose.dev.yml` (PostgreSQL 16, Redis 7, LiteLLM Proxy).
2. **Global Artifact Pool (Pydantic Schemas)**:
   - `packages/core/schemas/prd.py`: `ProductRequirementsDocument`, `UserStory`, `AcceptanceCriterion`.
   - `packages/core/schemas/contracts.py`: `RequirementsContract`, `PerformanceSLA`, `EdgeCaseSpecification`.
   - `packages/core/schemas/architecture.py`: `SystemArchitecture`, `ServiceComponent`, `APIEndpointSpec`.
   - `packages/core/schemas/data_models.py`: `DataArchitecture`, `TableDefinition`, `ColumnDefinition`, `MigrationStep`.
   - `packages/core/schemas/ux.py`: `UXSpecification`, `PageWireframe`, `UIComponentNode`, `DesignTokens`.
   - `packages/core/schemas/security.py`: `SecuritySpecification`, `ThreatModelEntry`, `AuthFlowSpec`.
   - `packages/core/schemas/tasks.py`: `TaskTicket` (with domain_tags), `TaskDAG`, `KanbanState`.
   - `packages/core/schemas/artifacts.py`: `ArtifactBundle`, `SprintReport`, `TokenUsageMetric`, `DeltaDocument`.
3. **Dynamic Provider Registry & Inference Routing**:
   - `packages/core/provider_registry.py` & `providers.yaml`: Configuration-driven registry with dynamic LiteLLM export and multi-tier cascading fallback logic.
4. **DSH A2A Interface Bridge**:
   - `packages/core/dsh_bridge.py`: Python $\leftrightarrow$ DSH A2A JSON-RPC client and central dispatcher for all 13 specialist agents.
5. **Centralized Configuration**:
   - `packages/core/config.py`: Type-safe application settings with Pydantic Settings.
6. **Automated Verification**:
   - Implemented unit test suite in `tests/unit/` (`test_schemas.py`, `test_provider_registry.py`, `test_dsh_bridge.py`, `test_config.py`).
   - **Verification Result**: 14/14 tests passing cleanly.

---

## [2026-08-25] Phase 1 — LangGraph Orchestration Engine & Checkpoint Persistence

### Objectives Achieved
1. **Multi-Agent Organizational State Definition**:
   - `packages/orchestrator/state.py`: Complete `OrgState` TypedDict capturing concept, PRD, 5 architect specifications, WBS/DAG, engineering artifacts, QA reviews, demo bundles, standup gates, and delta documents.
2. **Deterministic Graph Nodes**:
   - `packages/orchestrator/nodes.py`: Implemented 14 workflow nodes covering Product Strategy, Parallel Architect Pool (Requirements, System, Data, UX, Security), Engineering Management, Specialist Engineering, QA Verification, Demo Synthesis, Standup Gate, and Delta Replanning.
3. **StateGraph Workflow & Conditional Routing**:
   - `packages/orchestrator/graph.py`: Assembled StateGraph with parallel architect fan-out/fan-in, QA retry loop, and `interrupt_before=["standup_review"]` for Human-in-the-Loop governance.
4. **Checkpoint Persistence**:
   - `packages/orchestrator/checkpointer.py`: Support for `MemorySaver` (in-memory dev/test) and `PostgresSaver` (production state persistence).
5. **Swarm Circuit Breakers & Oscillation Guard**:
   - `packages/orchestrator/circuit_breaker.py`: Max retry thresholds per ticket and SHA256 code hash tracking to prevent cyclical code oscillation.
6. **Automated Verification**:
   - `tests/unit/test_orchestrator.py`: Full graph execution to standup gate, checkpoint resumption with executive steering feedback, and circuit breaker verification.
   - **Verification Result**: 17/17 tests passing cleanly with 0 warnings.
