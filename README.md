# DevCorp AI 🏢🤖

**Autonomous Multi-Agent Software Organization: Poly-Model Coordination, Standardized Protocols, Token Resilience, and Automated Demonstration Standup Systems.**

DevCorp AI is an enterprise-grade autonomous software engineering platform featuring:
- **Hierarchical Role Specialization**: 13 specialist agents across Product Management, Architecture, Engineering Management, Engineering, QA, and Demo Release.
- **DeepSeek Harness (`dsh`) Micro-Kernel Runtime**: Declarative Cordis plugin profiles (`cordis.yml`), native MCP tool connectivity, and A2A interoperability.
- **LangGraph Macro-Orchestrator**: Deterministic workflow state machine with PostgreSQL checkpoint persistence, budget guards, and Human-in-the-Loop (HITL) interrupt gates.
- **Token & Inference Resilience**: LiteLLM gateway with cascading multi-provider fallbacks (Gemini, Claude, GPT-4o, DeepSeek, local vLLM), Redis circuit breakers, and per-role token quotas.
- **Automated Standup Engine**: Headless Playwright UI journey recordings with visible cursor overlays, authenticated React dashboard, and Google Meet / Microsoft Teams standup bots.
- **Dual Deployment Architecture**: Docker Compose for rapid local development; Kubernetes (Helm charts) for production autoscaling.

---

## Repository Structure

```
devcorp-ai/
├── docs/                           # Canonical specifications & architecture
│   ├── architecture_reference.md   # Reference Architecture v2.1
│   ├── implementation_plan.md      # Phased Implementation Plan v2.1
│   └── deepseek_harness_comparison.md # DSH integration analysis
│
├── profiles/                       # 13 DSH Cordis Declarative Profiles (.cordis.yml)
├── prompts/                        # Specialist agent system prompts (.md)
│
├── packages/
│   ├── core/                       # Shared Pydantic schemas, DSH bridge, config
│   ├── orchestrator/               # LangGraph state machine & PostgreSQL checkpointer
│   ├── gateway/                    # LiteLLM proxy config & budget management
│   ├── mcp_servers/                # MCP server implementations (FS, Git, Terminal, Tests)
│   ├── demo_engine/                # Playwright demo synthesis pipeline
│   ├── dashboard/                  # Authenticated React dashboard & Trajectory Explorer
│   └── standup_integrations/       # Google Meet & Microsoft Teams standup bots
│
├── infra/
│   ├── docker/                     # Dockerfiles for DSH runtime, sandbox, vLLM
│   ├── compose/                    # Docker Compose files (dev, staging)
│   └── k8s/                        # Kubernetes Helm charts (prod)
│
└── tests/
    ├── unit/                       # Schema and unit test suites
    ├── integration/                # Service integration tests
    └── e2e/                        # End-to-end autonomous build tests (Expense Tracker)
```

---

## 13-Agent Specialist Swarm

| Tier | Role | Implementation Mode | Primary Output Artifact |
|:---|:---|:---|:---|
| **Tier 1** | **Product Manager** | DSH Profile (`product-manager.cordis.yml`) | `ProductRequirementsDocument` |
| **Tier 2** | **Requirements Architect** | DSH Profile (`architect-requirements.cordis.yml`) | `RequirementsContract` |
| **Tier 2** | **System Architect** | DSH Profile (`architect-system.cordis.yml`) | `SystemArchitecture` & OpenAPI 3.1 |
| **Tier 2** | **Data Architect** | DSH Profile (`architect-data.cordis.yml`) | `DataArchitecture` & SQL Migrations |
| **Tier 2** | **UX Architect** | DSH Profile (`architect-ux.cordis.yml`) | `UXSpecification` & JSON Wireframes |
| **Tier 2** | **Security Architect** | DSH Profile (`architect-security.cordis.yml`) | `SecuritySpecification` & STRIDE |
| **Tier 2/3**| **Agent Router** | DSH Profile (`agent-router.cordis.yml`) | Domain-tag Routing Decisions |
| **Tier 3** | **Engineering Manager** | DSH Profile (`engineering-manager.cordis.yml`) | `TaskDAG` & `KanbanState` |
| **Tier 4** | **Backend Engineer** | DSH Profile (`engineer-backend.cordis.yml`) | Server Source Code, Tests, Migrations |
| **Tier 4** | **Frontend / UI Engineer**| DSH Profile (`engineer-frontend.cordis.yml`) | React Code, CSS, Component Tests |
| **Tier 4** | **UX Engineer** | DSH Profile (`engineer-ux.cordis.yml`) | Design System Library, a11y Tests |
| **Tier 5** | **QA / Reviewer** | DSH Profile (`qa-reviewer.cordis.yml`) | Test Logs, Coverage, Review Verdicts |
| **Tier 6** | **Demo / Release Agent** | DSH Profile (`demo-release.cordis.yml`) | MP4 Walkthroughs, Playwright Traces |

---

## Documentation

- [Architecture Reference v2.1](docs/architecture_reference.md)
- [Implementation Plan v2.1](docs/implementation_plan.md)
- [DeepSeek Harness Comparison](docs/deepseek_harness_comparison.md)
- [Work Log & Version Control](WORKLOG.md)
