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

---

## [2026-08-25] Phase 2 & Phase 3 — Inference Gateway, DSH Runtime Profiles & MCP Servers

### Objectives Achieved
1. **Inference Gateway & Resilience Tier (Phase 2)**:
   - `packages/gateway/budgets.py`: Implemented granular per-role spend tracker and alert manager across all 13 roles (`NORMAL`, `SOFT_ALERT_80`, `CRITICAL_ALERT_95`, `HARD_HALT_100`).
   - `packages/gateway/circuit_breaker.py`: Implemented 3-state circuit breaker (`CLOSED`, `OPEN`, `HALF_OPEN`) with cooldown probing to protect the swarm from upstream provider rate limits (429) or outages.
   - `packages/gateway/litellm_config_generator.py`: Compiled provider registry into dynamic LiteLLM YAML configurations with cascading fallback chains.
2. **DSH Agent Runtime Profiles (Phase 3)**:
   - Created all 13 declarative Cordis profiles in `profiles/*.cordis.yml`:
     - *Tier 1*: `product-manager.cordis.yml`
     - *Tier 2 (Architects)*: `architect-requirements.cordis.yml`, `architect-system.cordis.yml`, `architect-data.cordis.yml`, `architect-ux.cordis.yml`, `architect-security.cordis.yml`
     - *Tier 2/3*: `agent-router.cordis.yml`
     - *Tier 3*: `engineering-manager.cordis.yml`
     - *Tier 4 (Engineers)*: `engineer-backend.cordis.yml`, `engineer-frontend.cordis.yml`, `engineer-ux.cordis.yml`
     - *Tier 5*: `qa-reviewer.cordis.yml`
     - *Tier 6*: `demo-release.cordis.yml`
3. **Model Context Protocol (MCP) Tool Servers**:
   - `packages/mcp_servers/filesystem_server.py`: `read_file`, `write_file`, `list_dir`, `search_files`.
   - `packages/mcp_servers/git_server.py`: `git_status`, `git_diff`, `git_commit`, `git_log`.
   - `packages/mcp_servers/terminal_server.py`: `run_command` in sandboxed bash.
   - `packages/mcp_servers/test_runner_server.py`: `run_tests`.
4. **Sandboxed Virtualization**:
   - `infra/docker/sandbox-agent.Dockerfile`: Ubuntu 24.04 container pre-configured with Python 3.12, Node.js 20, Git, and test frameworks for isolated execution.
5. **Automated Verification**:
   - `tests/unit/test_gateway.py`: Verified budget thresholds and circuit breaker state transitions.
   - `tests/unit/test_dsh_profiles.py`: Verified schema adherence and plugin configurations for all 13 DSH Cordis YAML profiles.
   - `tests/unit/test_mcp_servers.py`: Verified tool execution across all MCP servers.
   - **Verification Result**: 37/37 tests passing cleanly.

---

## [2026-08-25] Complete Platform Infrastructure Implementation (Phases 3A, 5, 6, 7, 8)

### Objectives Achieved
1. **Specialist Agent System Prompts (Phase 3A)**:
   - Authored all 13 comprehensive markdown system prompts in `prompts/` mapped to each role's Cordis profile.
   - Built `packages/core/prompt_loader.py` for automated prompt hydration.
2. **A2A Protocol & Discovery Layer (Phase 5)**:
   - `packages/a2a_layer/registry.py`: Dynamic skill-based agent registry aggregating cards from running DSH instances.
   - `packages/a2a_layer/task_manager.py`: Stateful task lifecycle manager (`submitted`, `working`, `input-required`, `completed`, `failed`).
3. **Automated Demo Synthesis Engine (Phase 6)**:
   - `packages/demo_engine/environment.py`: Ephemeral dev stack orchestrator (frontend: 3000, backend: 8000).
   - `packages/demo_engine/recorder.py`: Playwright video recorder with visible cursor tracking and interaction ripple overlays.
   - `packages/demo_engine/bundler.py`: Artifact bundle packager for MP4 walkthroughs, traces, and manifests.
4. **Executive Dashboard API & Video Standup Bots (Phase 7)**:
   - `packages/dashboard/api/main.py`: Production FastAPI backend with real-time SSE streaming (`/api/events/stream`), Kanban queries, budget monitoring, trajectory explorer, and executive feedback endpoints.
   - `packages/standup_integrations/google_meet_bot.py`: Google Meet standup bot for scheduling meetings and broadcasting chat summaries.
   - `packages/standup_integrations/ms_teams_bot.py`: Microsoft Teams Bot Framework integration with Adaptive Cards.
5. **Operational Guardrails & Kubernetes Helm Charts (Phase 8)**:
   - `packages/orchestrator/guardrails.py`: Schema contract validation and destructive sandbox command escape traps.
   - `infra/k8s/`: Complete Helm chart (`Chart.yaml`, `values.yaml`, `values.prod.yaml`, deployments, services, ingress).
6. **Comprehensive Automated Verification**:
   - `tests/unit/`: 14 test modules covering all layers (`test_a2a_layer.py`, `test_dashboard_api.py`, `test_demo_engine.py`, `test_dsh_profiles.py`, `test_gateway.py`, `test_guardrails.py`, `test_mcp_servers.py`, `test_orchestrator.py`, `test_prompts.py`, `test_provider_registry.py`, `test_schemas.py`, `test_standup_bots.py`, `test_config.py`, `test_dsh_bridge.py`).
   - **Verification Result**: 62/62 tests passing cleanly in 0.92s.
