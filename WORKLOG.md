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
