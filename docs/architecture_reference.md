# Architecture and Implementation of Autonomous Multi-Agent Software Organizations

## Reference Architecture Document (v2.1)

> **Purpose**: This document is the canonical architecture specification for the project. All implementation decisions should trace back to this document. Stored here to preserve full context across sessions.
>
> **v2.1 updates**: DeepSeek Harness (`dsh`) powered by the Cordis meta-framework integrated as the universal micro-kernel agent execution runtime for all 13 specialist agents; declarative YAML plugin profiles (`cordis.yml`), native MCP (`dsh-mcp`) and A2A (`dsh-a2a`) integration, append-only trajectory auditing, dual deployment (Docker Compose + Kubernetes), authenticated dashboard, Google Meet / Microsoft Teams standup integration, expense tracker reference application.

---

## Hierarchical Organizational Topology and Role Specialization

The realization of fully autonomous software development organizations requires translating the structural, procedural, and communicative hierarchies of large-scale engineering enterprises, such as Google, into multi-agent systems. Early attempts at autonomous code generation relied on unstructured conversational chains among generalist Large Language Models (LLMs), which frequently resulted in catastrophic context dilution, logical inconsistencies, and cascading hallucinations. In such naive setups, technical specifications degrade rapidly across successive handoffs, mirroring the informational decay of a telephone game. Overcoming these limitations necessitates shifting from conversational free-form dialogue to structured multi-agent architectures governed by Standardized Operating Procedures (SOPs) and an assembly-line paradigm.

### Enterprise Role Decomposition (13 Specialist Agents)

Production-grade autonomous software engineering requires deep specialization. A single "Enterprise Architect" cannot adequately cover database design, UX wireframing, security threat modeling, and API topology simultaneously. Similarly, a generic "Software Engineer" cannot produce expert-quality backend API code, accessible frontend components, and design-system utilities. The architecture decomposes Tier 2 (Architecture) and Tier 4 (Engineering) into domain-specific specialist roles, each executed as a discrete DeepSeek Harness (`dsh`) instance configured via a declarative YAML plugin profile (`cordis.yml`) with domain-specific system prompts, tool bindings, and output schemas.

#### Tier 1: Product Strategy and Requirement Engineering

* **Product Manager Agent**: Ingests ambiguous, high-level executive product visions and market requirements. Formalizes requirements into a structured Product Requirements Document (PRD) comprising comprehensive user stories, operational constraints, and explicit acceptance criteria. For delta replanning after executive feedback, performs semantic diff against existing PRD and produces a formal DeltaDocument.

#### Tier 2: Specialist Architecture (5 Agents)

* **Requirements Architect Agent**: Ingests the finalized PRD and formalizes user stories into testable contracts with Given/When/Then specifications, edge case identification, boundary conditions, constraint matrices (performance SLAs, data volume estimates, latency targets), and non-functional requirements mapped to testable acceptance criteria.

* **System Architect Agent**: Ingests the Requirements Contract and PRD, then translates business logic into concrete infrastructure topologies, service decomposition, API gateway designs, technology stack selections, and deployment architectures. Produces OpenAPI 3.1 specifications for all service interfaces, component diagrams, and sequence diagrams for critical user flows.

* **Data Architect Agent**: Ingests the Requirements Contract and System Architecture, then designs database schemas, data flow models, migration strategies, caching topologies, and data validation rules. Produces entity-relationship diagrams, SQL migration scripts, data flow diagrams, and validation schemas.

* **UX Architect Agent**: Ingests the PRD and User Stories, then creates information architecture, structured wireframes (as JSON component trees), design token systems (colors, typography, spacing, breakpoints), component hierarchies, responsive breakpoint strategies, and interaction flow diagrams.

* **Security Architect Agent**: Ingests the System Architecture and Data Schemas, then produces threat models (STRIDE analysis), authentication and authorization flow designs, data encryption strategies, compliance mappings, API security policies (rate limiting, input sanitization), and OWASP Top 10 checklists mapped to system components.

#### Tier 2 Dispatch: Agent Router

* **Agent Router**: A lightweight dispatch agent that examines PRD scope and ticket metadata to determine which subset of specialist architects and engineers to activate. A CLI tool might skip UX Architect entirely; a web application activates all five architects. Routes based on `domain_tags` assigned by the Engineering Manager (e.g., `["api", "db"]` → Backend Engineer, `["ui", "layout"]` → Frontend Engineer, `["a11y", "design-system"]` → UX Engineer). If a ticket spans multiple domains, the Router can split it or assign a primary with a secondary reviewer.

#### Tier 3: Engineering Management and Task Scheduling

* **Engineering Manager Agent**: Ingests all architect outputs and compiles a Work Breakdown Structure (WBS). The WBS is organized into a Directed Acyclic Graph (DAG) of interdependent atomic task tickets dispatched onto a virtual Kanban board. Each ticket is tagged with `domain_tags` for routing to the appropriate specialist engineer. Assigns estimated complexity (S/M/L) and sprint allocation. Handles escalations from QA circuit breakers and mediates architect disagreements.

#### Tier 4: Specialist Engineering (3 Agents)

* **Backend Engineer Agent**: Consumes backend-tagged tickets (API, database, server-side logic, scraping/parsing) and implements server-side codebases within isolated execution sandboxes. Implements FastAPI endpoints matching OpenAPI contracts, database queries, ORM models, migration scripts, and domain-specific logic (e.g., bank statement parsing pipelines, transaction categorization).

* **Frontend / UI Engineer Agent**: Consumes frontend-tagged tickets (UI components, styling, responsive layouts, state management) and implements React components matching wireframe specifications, applies design token systems, builds responsive layouts, integrates with backend API endpoints, and writes component tests.

* **UX Engineer Agent**: Consumes UX-tagged tickets (accessibility, design system, interaction patterns) and implements the design system as a component library, ensures WCAG 2.1 AA compliance, builds interaction patterns (drag-to-recategorize, swipe gestures), and implements loading states, error states, and empty states.

#### Tier 5: Quality Assurance and Code Review

* **QA and Reviewer Agents**: Evaluate code diffs against static analysis suites (ruff, mypy, eslint), security benchmarks, acceptance criteria from tickets, and dynamic end-to-end integration tests. Drive deterministic self-correction debugging loops. On rejection, generate specific, actionable feedback for the specialist engineer retry.

#### Tier 6: Demo Synthesis and Sprint Aggregation

* **Demo and Release Agent**: Orchestrates local service environments, executes automated headless user journeys via Playwright, generates video recordings with visible interaction overlays, and prepares sprint demonstrations for executive evaluation.

#### Executive Steering Layer

* **Human Executive**: Participates exclusively at designated sprint and standup checkpoints — via the authenticated web dashboard or a Google Meet / Microsoft Teams standup meeting — to review visual demos and submit high-level strategic feedback without managing routine ticket workflows.

### Complete Role Reference Table

| Tier / Role | Operational Responsibilities | Primary Input Artifacts | Generated Output Artifacts | Target Foundation Model Profile |
| :---- | :---- | :---- | :---- | :---- |
| **Product Manager (PM)** | Market requirement analysis, user journey definition, acceptance criteria synthesis, delta replanning | High-level executive concepts, strategic business goals | Structured PRD (JSON/Markdown), User Story Backlog, DeltaDocument | Ultra-long context window, high-level abstract reasoning, multi-turn synthesis |
| **Requirements Architect** | Formalizes PRD into testable contracts, edge case identification, constraint matrices | Validated PRD | Requirements Contract (formal specs, SLAs, constraints matrix) | High structural reasoning, formal specification generation |
| **System Architect** | Infrastructure topology, service decomposition, API design, tech stack selection | Requirements Contract, PRD | OpenAPI 3.1 Specs, Component Diagrams, Sequence Diagrams, Deployment Topology | High structural reasoning, strict schema adherence, systems logic |
| **Data Architect** | Database schema design, data flow modeling, migration strategies, caching topology | Requirements Contract, System Architecture | ER Diagrams, SQL Migrations, Data Flow Diagrams, Validation Schemas | Schema design precision, relational modeling, data flow analysis |
| **UX Architect** | Information architecture, wireframes, design tokens, component hierarchy, responsive strategy | PRD, User Stories | Wireframes (JSON), Design Token Definitions, Component Tree, Interaction Flows | Multimodal reasoning (preferred), UI/UX domain knowledge |
| **Security Architect** | Threat modeling, auth flow design, encryption strategy, compliance mapping | System Architecture, Data Schemas | Threat Model, Auth Flow Specs, Security Policy, OWASP Checklist | Security domain knowledge, threat analysis reasoning |
| **Agent Router** | Domain-based ticket dispatch to specialist architects and engineers | Ticket metadata, agent registry | Routing decision (target agent ID + rationale) | Fast structured classification, low reasoning demand |
| **Engineering Manager** | WBS task decomposition, dependency DAG, sprint planning, domain-tagged ticket creation | All Architect outputs | Task Dependency DAG, Domain-Tagged Tickets, Kanban State | Deterministic scheduling, constraint optimization, dependency resolution |
| **Backend Engineer** | API implementation, business logic, database queries, server-side integrations, scraping/parsing | Backend-tagged tickets, OpenAPI specs, DB schemas | Server-side Source Code, API Tests, Migration Scripts | Top-tier SWE-bench performance, tool execution precision, bash fluency |
| **Frontend / UI Engineer** | React components, CSS/styling, responsive layouts, state management, API integration | Frontend-tagged tickets, wireframes, design tokens, OpenAPI specs | Frontend Source Code, Component Tests, Storybook Stories | Frontend framework expertise, visual reasoning |
| **UX Engineer** | Accessibility compliance, design system implementation, interaction patterns, progressive enhancement | UX-tagged tickets, design tokens, wireframes | Design System Code, a11y Tests, Interaction Utilities | Accessibility standards knowledge, design system expertise |
| **QA / Test Engineer** | Static analysis, integration tests, security scans, code review, cross-browser testing | Code Diffs, Acceptance Criteria, Live Environment | Test Execution Logs, Coverage Reports, Defect Issues, Review Verdicts | Edge-case generation, fault injection, compiler log parsing |
| **Demo / Release Engineer** | Service orchestration, mock data seeding, automated UI journey recording | Validated Codebase, PRD User Stories | Video Replays (.mp4), Playwright Traces, Live Web Sandbox, Demo Bundles | UI automation script generation, DOM navigation |

### Standardized Message Exchange via Global Artifact Pools

Structured communication protocols eliminate information distortion across agent handoffs. Rather than transmitting unconstrained natural language prompts, the architecture implements a publish-subscribe global message pool. Agents publish their structured documents into this centralized repository, and downstream agents subscribe only to the specific artifact types required for their operational roles.

With 13 specialist agents, the artifact pool schema expands to include domain-specific intermediate artifacts:

| Artifact Type | Producer | Consumers |
| :---- | :---- | :---- |
| ProductRequirementsDocument | Product Manager | All Architects, Agent Router |
| RequirementsContract | Requirements Architect | System Architect, Data Architect, Security Architect, Engineering Manager |
| SystemArchitecture | System Architect | Data Architect, Security Architect, Engineering Manager, Backend Engineer |
| DataArchitecture | Data Architect | Backend Engineer, Engineering Manager |
| UXSpecification | UX Architect | Frontend Engineer, UX Engineer, Engineering Manager |
| SecuritySpecification | Security Architect | All Engineers, QA |
| TaskTicket (domain-tagged) | Engineering Manager | Agent Router → Specialist Engineers |
| TaskDAG | Engineering Manager | Orchestrator |
| KanbanState | Engineering Manager | Orchestrator, Dashboard |
| ArtifactBundle | Demo Agent | Dashboard, Standup Bot |
| SprintReport | Orchestrator | Dashboard, Standup Bot |
| DeltaDocument | Product Manager | All Architects, Engineering Manager |
| ProviderConfig | Admin (human) | Gateway, All Agents |

---

## Open-Source Enterprise Stack and Protocol Architecture

Building a production-grade multi-agent software enterprise requires an open-source, vendor-agnostic foundation that decouples macro agent orchestration, horizontal agent-to-agent collaboration, micro runtime execution, vertical tool integration, and inference routing.

| Enterprise Function | Open-Source Component | License | Architectural Role |
| :---- | :---- | :---- | :---- |
| **Macro Workflow State Machine** | **LangGraph** | MIT | Coordinates deterministic role transitions, conditional loops, checkpoint persistence, fan-out/fan-in for parallel architect and engineer execution, and human-in-the-loop interrupts. |
| **Micro Agent Execution Runtime** | **DeepSeek Harness (dsh)** | MIT | Micro-kernel agent runtime built on the **Cordis** meta-framework. Implements an "everything is a plugin" architecture where model adapters, tool registries, sandboxes, session states, and execution loops are composable, swappable plugins. |
| **Agent Execution Auditing** | **DSH Trajectory System** | MIT | Append-only event logging subsystem recording every reasoning step, tool invocation, sub-agent dispatch, and token metric. Enables historical replays, forking, and deep inspection. |
| **Inter-Agent Messaging** | **Agent-to-Agent Protocol (A2A) via `dsh-a2a`** | Apache-2.0 / MIT | Standardizes cross-agent discovery via JSON Agent Cards (13 cards for 13 specialist roles), asynchronous task state machines, fan-out task groups, and multi-part artifact handoffs out-of-the-box. |
| **Tool & Resource Layer** | **Model Context Protocol (MCP) via `dsh-mcp`** | Open Standard / MIT | Provides structured JSON-RPC interfaces over stdio/SSE to expose local file systems, compilers, and Git operations to LLMs through declarative configuration. |
| **Sandboxed Execution** | **Docker / SmolVM (Firecracker) via DSH Sandbox Plugin** | Apache-2.0 / MIT | Containerized and hardware-isolated execution environments providing Standard (shell+web), Code (programmatic SDK batch calls), and Minimal modes. |
| **Local Inference Serving** | **vLLM / Ollama** | Apache-2.0 | Serves local open-weight coding and reasoning models with high-throughput PagedAttention and OpenAI-compatible endpoints. Configurable — enabled only when local GPU is available. |
| **Resilience & Budget Proxy** | **LiteLLM Proxy** | MIT | Central gateway managing provider load balancing, automated 429 rate-limit failovers, spend budgets, circuit breakers, and dynamic provider registry. |
| **Scalable Provider Registry** | **Custom YAML-based ProviderRegistry** | Internal | Configuration-driven LLM provider management — add any provider by appending a YAML entry, no code changes required. |
| **Automated Demo Engine** | **Playwright** | Apache-2.0 | Drives sandboxed Chromium instances, executes PRD user journeys, renders visible interaction indicators, and records MP4 demos. |
| **Standup Dashboard** | **React + Vite + TypeScript** | MIT | Real-time authenticated dashboard rendering active Kanban boards, live demo playback, token/cost monitoring, DSH trajectory explorer, and feedback input channels via SSE. |
| **Video Standup Integration** | **Google Meet API / Microsoft Teams Bot Framework** | Proprietary APIs | Bot-based standup hosting — joins meetings, shares demo videos, posts sprint summaries, transcribes executive feedback. Configurable per organization. |
| **Authentication** | **OAuth2/OIDC (Google, GitHub SSO)** | Open Standard | Production-grade authentication for the standup dashboard with role-based access control. |
| **Dev Deployment** | **Docker Compose** | Apache-2.0 | Local development orchestration for all services. |
| **Prod Deployment** | **Kubernetes (Helm)** | Apache-2.0 | Production deployment with HPA scaling, health checks, TLS ingress, and persistent volumes. |

---

## DeepSeek Harness (dsh) as Agent Runtime

DeepSeek Harness (`dsh`) serves as the universal execution runtime for every individual agent in the organization, replacing monolithic, hardcoded agent implementations with a composable micro-kernel design powered by the **Cordis** meta-framework.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        LangGraph (Python Macro Layer)                  │
│   • Organizational State Machine        • Thread Checkpointing (Postgres)│
│   • Sprint & Kanban Coordination        • HITL Interrupts & Standup Gate │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ A2A Task Delegation (HTTP / SSE)
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 DeepSeek Harness (dsh Instance - Micro Layer)          │
│                                                                        │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                      Cordis Micro-Kernel Core                  │   │
│   └───────┬──────────────┬──────────────┬──────────────┬───────────┘   │
│           │              │              │              │               │
│           ▼              ▼              ▼              ▼               ▼
│     ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│     │dsh-model │   │ dsh-mcp  │   │ dsh-a2a  │   │dsh-sand- │   │dsh-tra-  │
│     │(LiteLLM) │   │ (Tools)  │   │ (Cards & │   │box       │   │jectory   │
│     │          │   │          │   │  Tasks)  │   │(Runtime) │   │(Audit)   │
│     └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
└────────────────────────────────────────────────────────────────────────┘
```

### Core Architecture: Cordis Meta-Framework & Spatiotemporal Composability

Unlike monolithic agent frameworks where agent loops and tool invocations are tightly coupled, DSH is built on the formal paradigm of **spatiotemporal composability**:

* **Micro-Kernel with No Privileged Core**: There is no hardcoded agent loop to patch. Models, tool registries, sandboxes, session state, UI components, and the agent loop itself are isolated plugins mounted onto a shared context tree composed at boot time.
* **Spatial Composability**: Plugins declare typed service contracts and event listeners. The dependency graph dynamically accommodates plugin swaps (e.g., changing model providers or adding an AST analysis plugin) without breaking surrounding modules.
* **Temporal Composability (Revertible Effects)**: When a plugin is unmounted or updated, all its modifications to the execution context (timers, file descriptors, event listeners) are cleanly and reversibly dismantled without residual memory leaks.

### Declarative Agent Profiles (`cordis.yml`)

Each of the 13 specialist agents is instantiated by loading a declarative profile that defines its exact capabilities, toolsets, and system prompts:

```yaml
# profiles/engineer-backend.cordis.yml
name: "engineer-backend"
version: "1.0.0"

plugins:
  # Model routing through centralized LiteLLM Gateway
  - name: "dsh-model-litellm"
    config:
      endpoint: "http://litellm-proxy:4000/v1"
      model: "primary/reasoning"
      api_key: "${LITELLM_MASTER_KEY}"
      temperature: 0.1

  # Native Model Context Protocol server bindings
  - name: "dsh-mcp"
    config:
      servers:
        - name: "filesystem"
          transport: "stdio"
          command: "mcp-server-filesystem"
          args: ["--root", "/workspace"]
        - name: "git"
          transport: "stdio"
          command: "mcp-server-git"
        - name: "terminal"
          transport: "stdio"
          command: "mcp-server-terminal"
        - name: "test-runner"
          transport: "stdio"
          command: "mcp-server-test-runner"

  # Native Agent-to-Agent protocol communication
  - name: "dsh-a2a"
    config:
      server: true
      port: 8080
      card:
        name: "backend-engineer-agent"
        description: "Implements backend APIs, database schemas, and scraping pipelines"
        skills:
          - id: "implement-backend-ticket"
            name: "Backend Implementation"
            inputModes: ["application/json"]
            outputModes: ["application/json", "text/plain"]

  # Ephemeral sandbox isolation
  - name: "dsh-sandbox"
    config:
      mode: "standard"
      image: "agent-sandbox:backend-python-node"
      timeout_seconds: 1800

  # Append-only execution auditing
  - name: "dsh-trajectory"
    config:
      output_dir: "/trajectories/backend-engineer"
      format: "jsonl"
      record_tokens: true
```

### Trajectory Logging and Deep Execution Auditing

Every DSH instance automatically maintains an append-only event log. Every intermediate reasoning token, tool invocation (with exact JSON parameters), stdout/stderr response, and sub-agent dispatch is recorded sequentially.

These trajectory logs are streamed directly to the **Standup Dashboard** and archived with sprint reports, enabling:
1. **Historical Replay**: Re-running execution trajectories step-by-step to diagnose bugs.
2. **Trajectory Forking**: Branching an agent's execution from step $N$ with an alternative prompt or tool output.
3. **Deterministic Benchmarking**: Measuring token efficiency and tool success rates across agent iterations.

### Sub-Agent Delegation & Multi-Harness Composition

Because DSH treats external agent harnesses as plugins, individual specialist agents can dynamically spawn and delegate to specialized sub-agents (e.g., invoking Claude Code for rapid refactoring or Codex for AST translations) within their isolated execution trajectory while preserving unified auditing.

---

## The A2A and MCP Protocol Layer

### The A2A Inter-Agent Protocol Layer (via `dsh-a2a`)

The Agent-to-Agent (A2A) protocol serves as the horizontal inter-agent messaging tier. A2A standardizes how autonomous agents discover each other's capabilities, negotiate delegation, exchange structured data, and track long-running tasks across heterogeneous platforms and model boundaries.

In this architecture, A2A compliance is provided natively by the `dsh-a2a` plugin mounted in each agent's DSH instance:
* **Skill-Based Discovery**: Every agent exposes its Agent Card at `/.well-known/agent.json`. The Agent Router queries the registry to resolve which agent can handle specific task requirements.
* **Stateful Tasks**: Workflows execute as stateful Tasks with discrete lifecycle states: `submitted`, `working`, `input-required`, `completed`, and `failed`.
* **Fan-Out Task Groups**: Supported natively for parallel architect (Tier 2) and parallel engineer (Tier 4) execution streams.

### The MCP Tooling and Environment Layer (via `dsh-mcp`)

While A2A governs horizontal communication between independent agents, the Model Context Protocol (MCP) standardizes vertical communication between an individual agent and its physical execution environment.

The `dsh-mcp` plugin connects DSH instances directly to MCP servers over stdio or SSE without requiring custom client boilerplate code:

| MCP Server | Exposed Tools | Primary Agent Consumers |
| :---- | :---- | :---- |
| `filesystem` | `read_file`, `write_file`, `list_dir`, `search_files` | Backend Engineer, Frontend Engineer, UX Engineer, QA |
| `git` | `status`, `diff`, `commit`, `log`, `branch` | All Engineers, QA, Demo |
| `terminal` | `run_command` (sandboxed bash) | All Engineers, QA, Demo |
| `test_runner` | `run_tests`, `get_coverage` | All Engineers, QA |
| `browser` | `navigate`, `screenshot`, `click`, `fill` | Demo Agent |

| Architectural Dimension | Model Context Protocol (MCP) | Agent-to-Agent Protocol (A2A) |
| :---- | :---- | :---- |
| **Core Operational Objective** | Standardizes agent-to-tool and agent-to-resource integrations | Standardizes autonomous agent-to-agent coordination and delegation |
| **Origin & Open Stewardship** | Open Standard (Anthropic origin) | Open Standard (Linux Foundation / Google Cloud origin) |
| **Capability Discovery Mechanism** | Static/dynamic tool listing (`tools/list` JSON-RPC methods) | Dynamic JSON "Agent Cards" exposed at `.well-known/agent.json`; skill-based queries |
| **Message & Payload Abstraction** | Function execution requests and direct data resource URIs | Multi-part messages, task state machines, fan-out task groups, and structured artifacts |
| **State & Lifecycle Management** | Ephemeral, synchronous call-and-response execution | Long-running, asynchronous task lifecycles with state tracking |
| **System Boundary Focus** | Internal execution environment (local files, DBs, terminals) | External and cross-agent federation across diverse systems |

---

## Scalable LLM Provider Registry and Inference Architecture

### Configuration-Driven Provider Management

The system employs a YAML-based Provider Registry that decouples LLM provider configuration from application code. Adding a new LLM provider requires appending an entry to `providers.yaml` — no code changes, no redeployment of the gateway. Each provider entry specifies:

* Provider name and model identifier
* API endpoint and authentication method (API key, bearer token, or none for local)
* Tier classification (`primary`, `secondary`, `local`)
* Capability tags (`reasoning`, `coding`, `multimodal`)
* Enabled/disabled toggle
* Context window size and cost-per-token pricing

### Configurable Local GPU Fallback

The local vLLM inference tier is optional and configuration-driven. When a local GPU is available, the administrator sets `enabled: true` for the local provider entry, and it participates in the fallback cascade. When no local GPU is configured, the system skips the local tier entirely and continues cascading through cloud providers.

### Cascading Fallback Architecture

All LLM calls from every agent are routed through the LiteLLM Gateway proxy. The proxy enforces unified load balancing, dynamic retries, rate-limit management, and cascading model fallbacks:

* **Rate-Limit Interception and Cooldown**: When an upstream provider returns an HTTP 429 rate limit or quota exhaustion error, LiteLLM intercepts the exception, places the primary provider into a temporary cooldown window (rolling backoff), and transparently routes the pending request to the configured secondary fallback model within milliseconds.

* **Cascading Model Downgrade Hierarchy**:
  * *Primary Cloud Tier (High Reasoning / Large Context)*: Gemini 2.5 Pro, Claude Sonnet 4, or GPT-4o for PRD formulation, deep architectural design, and complex bug isolation.
  * *Secondary Cloud Tier (High-Throughput / Burst Capacity)*: Groq Llama-3.3-70B, OpenRouter pools, or DeepSeek Coder when primary cloud allocations face burst throttling.
  * *Local Tier (Zero-Cost Fallback, if configured)*: Local vLLM instances serving Qwen 2.5 Coder 32B or Devstral, providing unmetered execution immune to external API outages and rate limits. Skipped if not configured.
  * *Tertiary Cloud Tier*: If local is unavailable, cascade continues to the cheapest available enabled cloud provider in the registry.

* **Redis-Backed Circuit Breakers**: The gateway maintains a Redis-backed circuit breaker pattern across three operational states:
  * *CLOSED (Normal Operation)*: All model inference requests route directly through active providers.
  * *OPEN (Fast-Fail and Divert)*: If consecutive provider failures or latency spikes breach predefined thresholds (e.g., 5 consecutive errors), the circuit trips to OPEN, diverting traffic to local vLLM (if configured) or the cheapest available cloud provider.
  * *HALF-OPEN (Probing Recovery)*: After a configured recovery timeout (e.g., 60 seconds), single probe requests test the upstream provider's health; upon success, normal routing resumes.

### Hierarchical Token Budgeting and Spend Guardrails (13 Roles)

To prevent runaway loops from depleting financial allocations, LiteLLM enforces granular token and cost controls across all 13 agent roles:

| Agent Role | TPM Limit | RPM Limit | Monthly Budget Cap |
| :---- | :---- | :---- | :---- |
| Product Manager | 200K | 30 | $50 |
| Requirements Architect | 150K | 25 | $40 |
| System Architect | 200K | 30 | $50 |
| Data Architect | 150K | 25 | $40 |
| UX Architect | 150K | 25 | $40 |
| Security Architect | 100K | 20 | $30 |
| Engineering Manager | 100K | 20 | $30 |
| Agent Router | 50K | 60 | $15 |
| Backend Engineer (×N) | 500K | 60 | $200 |
| Frontend/UI Engineer (×N) | 400K | 50 | $150 |
| UX Engineer | 200K | 30 | $60 |
| QA / Reviewer | 300K | 40 | $80 |
| Demo / Release | 100K | 20 | $30 |
| **Total ceiling** | | | **~$815/month** |

* **Soft Alert Thresholds (80% and 95%)**: Reaching 80% triggers automatic traffic shaping, routing non-critical requests to local or cheaper models. Reaching 95% triggers an escalation alert logged to the standup ledger.
* **Hard Budget Ceilings (100%)**: Reaching 100% halts the execution graph and transitions the task to input-required standby, awaiting human budget expansion during standup.

### Context Window Saturation and Checkpoint Recovery

Extended development sessions risk context degradation, attention dilution, and token limit exceptions. The system manages memory and context boundaries systematically:

* **LangGraph Graph Checkpointing**: The full state of the multi-agent graph — including task status, ticket metadata, generated artifacts, active architect/engineer lists, and execution logs — is persisted after every node transition into a PostgreSQL checkpoint store. Agents do not pass unbounded conversation histories.
* **DSH Trajectory Compression**: When an engineering agent completes an implementation phase, DSH compresses raw shell and debugging outputs into structured semantic summaries. The full repository state remains on the file system rather than inside the LLM prompt context.
* **Standby and Resumption Mechanics**: If an agent exhausts its local context or encounters an unrecoverable quota ceiling, LangGraph serializes the execution thread to disk and enters a paused state. When resources are replenished or a fallback model is designated, execution resumes from the exact checkpoint without repeating prior development cycles.

---

## Execution Runtimes, Sandboxing, and Deterministic Self-Correction

### Sandboxed Virtualization Architecture

Autonomous agents require the ability to run arbitrary shell commands, install dependencies, compile binaries, and launch local web services. Executing unvetted agent commands on the host environment introduces critical security and stability risks.

The architecture isolates execution across two virtualization layers managed by the DSH Sandbox Plugin:

* **Containerized Docker Sandboxes (Primary)**: Managed via DSH's sandbox plugin, each agent session operates within an ephemeral container pre-configured with language runtimes (Python 3.12+, Node 20+), package managers, and development utilities. Network isolation prevents outbound internet access by default (allowlist for package registries). Auto-cleanup after session ends or timeout.
* **Hardware-Isolated MicroVMs (SmolVM / Firecracker, Optional)**: For tasks requiring kernel-level network emulation, multi-service topologies, or strict multi-tenant isolation, the system provisions lightweight KVM microVMs. MicroVMs boot in sub-second intervals, provide independent virtual network interfaces, and prevent container-breakout vulnerabilities. Enabled only when KVM is available on the host.

### Deterministic Feedback Loops and Performance Baselines

Coding agents operate under the ReAct paradigm augmented by deterministic compiler and test feedback. Code completion is never validated by LLM self-confidence alone. Instead, the agent executes unit test suites and build runners inside its sandbox. Compiler errors, standard error streams, and failed assertions are captured and fed directly back into the agent's observation window. The agent refactors the code iteratively until all tests pass cleanly or a circuit breaker terminates the loop (max 5 iterations, then escalate to Engineering Manager).

| Multi-Agent Framework / Agent Architecture | Benchmark Verification Score | Efficiency Metrics | Human Intervention Metric | Primary Architectural Paradigm |
| :---- | :---- | :---- | :---- | :---- |
| **MetaGPT** | 85.9% (HumanEval Pass@1), 87.7% (MBPP Pass@1), 3.75/4.0 Executability | 124.3–126.5 tokens per line of code | Human revision cost: 0.83 (scale 0-3) | Standardized Operating Procedures (SOPs), Assembly Line, Global Msg Pool |
| **ChatDev** | 2.25/4.0 Executability baseline score | 248.9 tokens per line of code | Human revision cost: 2.50 (scale 0-3) | Multi-turn Chat Chains, Memory Streams, Waterfall Phase Decomposition |
| **DeepSeek Harness (dsh + Cordis)** | High modular execution efficiency, configurable runtimes | Sub-second plugin mounting, batch tool mode | Low; full trajectory auditability and replay | Micro-kernel, Everything-is-a-Plugin, Spatiotemporal Composability |
| **OpenHands (CodeAct 2.1 + Claude 3.5)** | 53.0% (SWE-bench Verified), 41.7% (SWE-bench Lite) | High-throughput parallel tool calling | Low; fully automated pull-request resolution | Event-Stream Architecture, Docker Sandboxing, Software Agent SDK |
| **Mini-SWE-Agent** | >74.0% (SWE-bench Verified) | Ultra-minimal footprint (~100 lines Python core) | Autonomous execution on GitHub issue tickets | Purpose-built Agent-Computer Interface (ACI), concise context management |

---

## Asynchronous Standup Demonstration Engine and Human-on-the-Loop Governance

### The Human Executive Interaction Model

The platform operates under a Human-on-the-Loop governance model. The human stakeholder does not manage day-to-day coding, ticket triage, or manual code reviews. Instead, the human acts as an executive sponsor, engaging with the system through two channels:

1. **Authenticated Web Dashboard**: A production-hosted React application with OAuth2/OIDC authentication (Google SSO, GitHub SSO) providing real-time Kanban oversight, demo video playback, token/cost monitoring, DSH trajectory explorer, and strategic feedback submission via SSE.

2. **Video Standup Meetings (Google Meet / Microsoft Teams)**: A configurable standup bot that creates calendar meetings, joins the call, shares demo videos via screen share, posts sprint summary cards, and transcribes executive feedback for delta replanning. The organization chooses their preferred platform via configuration.

To facilitate this without blocking autonomous background operations, the orchestration layer utilizes Human-in-the-Loop (HITL) execution interrupts. Upon reaching a defined milestone (e.g., epic completion or demo preparation), LangGraph triggers an input-required state interrupt. The system serializes execution state to PostgreSQL/Redis, saves a checkpoint, and dispatches invitations via both SSE (dashboard) and calendar API (Meet/Teams).

### Video Standup Integration

The standup bot integration supports configurable video conferencing platforms:

**Google Meet flow**:
* Creates meetings via Google Calendar API with sprint agenda.
* Bot joins meeting and shares screen with demo MP4 playback.
* Posts sprint summary and Kanban snapshot into meeting chat.
* Records meeting for async review.

**Microsoft Teams flow**:
* Creates meetings via Microsoft Graph API.
* Bot joins via Teams Bot Framework SDK.
* Shares Adaptive Cards with sprint metrics, demo video links, and feedback forms.
* Posts meeting summary to a designated Teams channel.

The executive can provide feedback either verbally during the meeting (transcribed by the bot) or via the dashboard feedback form. Both pathways feed into the same delta-replanning pipeline.

### Automated Demo Synthesis Pipeline

To prevent agents from passing mocked unit tests on broken visual applications, the system includes an automated visual demo synthesis engine driven by Playwright:

1. **Ephemeral Environment Boot**: The Demo Agent boots the complete multi-tier application stack (frontend on port 3000, backend API on port 8000, and seeded database fixtures) inside an isolated sandbox container.
2. **User Journey Script Synthesis**: The Demo Agent translates PRD acceptance criteria and user stories into structured Playwright automation scripts. For the expense tracker reference application, this includes journeys for: statement upload, transaction review, category management, budget dashboard, and report export.
3. **Headless Execution with Visual Overlays**: The script runs inside a sandboxed Chromium instance with video capture and visible cursor tracking enabled (`record_video=True`, `show_cursor=True`). The browser renders a visible cursor indicator that mirrors mouse movements, animates click ripples, fills out form inputs, and transitions views.
4. **Demonstration Bundle Packaging**: Upon script completion, Playwright exports an MP4 video recording, HTML trace files, and DOM snapshots into a demo bundle accessible via the web dashboard and shareable in standup meetings.

### Interactive Standup Dashboard and Delta-Replanning

When the human executive enters the authenticated standup dashboard, the interface renders:

* An embedded, high-definition MP4 video demonstrating all newly developed features in action.
* A live interactive sandbox URL (or embedded noVNC stream) allowing immediate hands-on testing of the running container.
* An executive summary table detailing completed user stories, test coverage metrics, token consumption per role, and identified blockers.
* **Agent Trajectory Explorer**: Real-time browsing and historical replay of DSH trajectory event logs for deep inspection of agent decisions.
* A strategic feedback input form where the human inputs high-level steering directives (e.g., *"Simplify the navigation sidebar into a compact collapsible drawer and switch the authentication flow to passwordless magic links"*).
* Per-role token and cost monitoring with budget gauges and alert indicators.
* Real-time agent activity log streamed via SSE.

Submitting feedback initiates an automated delta-replanning sequence: the PM agent performs a semantic diff against the PRD, generating a formal requirement changelog; the relevant specialist architects (Requirements, System, Data, UX, Security — as determined by the Agent Router) update their respective specifications; and the Engineering Manager updates the task DAG and enqueues newly prioritized, domain-tagged tickets onto the Kanban board. The state machine unpauses, returning execution to the autonomous agent swarm.

| Standup Lifecycle Event | Automated Agent System Deliverable | Verification Artifact | Human Executive Governance Action |
| :---- | :---- | :---- | :---- |
| **Sprint Review & Demo** | Automated MP4 feature walkthrough video, live sandbox container URL, Meet/Teams screen share | Playwright trace archives, video recordings, live container endpoints | Evaluates UX alignment, validates visual aesthetics, reviews feature completeness |
| **Velocity & Resource Audit** | Sprint burndown tracking, completed ticket metrics, per-role token usage | Virtual Kanban board state, Git commit logs, real-time cost charts per agent | Inspects milestone velocity and approves compute resource consumption |
| **Blocker Escalation** | Root-cause analysis of failing tests, dependency conflicts, architect disagreements, or ambiguous specs | Standard error logs, failed assertion dumps, agent debate logs, DSH trajectory replays | Resolves business logic ambiguities, updates project scope, unblocks tasks |
| **Delta Steering & Resumption** | Structured Delta Document, updated PRD, updated architect specs, regenerated WBS task queue | Git diff of requirements, updated OpenAPI specs, modified task DAG | Submits natural language steering directives via dashboard form or meeting chat; approves resumption |

---

## Reference Application: Expense Tracker with Bank Statement Scraping

The system's end-to-end capabilities are validated against a reference application: a personal expense tracking web application with the following product vision:

> Build a personal expense tracking web application that lets users upload bank statements (PDF or CSV), automatically extracts and categorizes transactions, and provides visual dashboards for spending analysis.

**Core Features**:
1. User authentication (email/password + Google OAuth)
2. Bank statement upload (PDF and CSV support)
3. Automated transaction extraction from uploaded statements
4. Smart transaction categorization (groceries, dining, transport, utilities, etc.)
5. Manual category override with learning
6. Monthly/weekly spending dashboard with charts
7. Budget setting per category with alerts
8. Export reports as PDF

This application exercises the full specialist agent hierarchy: Requirements Architect (parsing edge cases, transaction formats), System Architect (upload pipeline, API design), Data Architect (transactions schema, categorization models), UX Architect (upload flow wireframes, dashboard charts), Security Architect (file upload validation, financial data encryption), Backend Engineer (PDF parsing, categorization logic), Frontend Engineer (dashboard charts, responsive layout), and UX Engineer (accessibility, design system).

---

## Systemic Failure Modes, Safety Guardrails, and Economic Optimization

Autonomous multi-agent systems operating over long durations encounter distinct failure modes that require algorithmic and operational guardrails:

* **Semantic Drift and Context Dilution**: Cumulative conversation histories degrade agent attention and generate hallucinated API signatures. Mitigated via strict Context Partitioning: agents receive only their immediate system prompt, immutable OpenAPI contracts, relevant file context retrieved via semantic AST search, and the active task ticket.
* **Infinite Execution Loops and Semantic Oscillation**: Autonomous debugging agents can oscillate between contradictory code edits. Enforced through deterministic Circuit Breakers: tasks are limited to five self-debug iterations before escalating to the Engineering Manager, and AST difference hashing terminates circular syntax states immediately.
* **Architect Disagreement**: Multiple specialist architects may produce conflicting specifications (e.g., System Architect's API design conflicts with Security Architect's access policies). Mitigated by Engineering Manager mediation: EM performs conflict detection across architect outputs and escalates to PM for resolution if automated mediation fails.
* **Wrong Specialist Routing**: Agent Router may dispatch a ticket to the wrong specialist engineer. Detected during QA review when implementation shows domain mismatch. QA re-tags the ticket and Agent Router re-dispatches to the correct specialist.
* **Security and Code Provenance**: Autonomous terminal commands can introduce vulnerabilities or execute destructive commands. Prevented by executing all actions within non-root Docker or SmolVM microVM sandboxes lacking access to host networks, while logging all operations to the DSH append-only trajectory audit ledger.
* **Provider Outage with No Local GPU**: When the circuit breaker trips to OPEN and no local vLLM tier is configured, the system cascades to the cheapest available cloud provider in the registry rather than halting entirely. If all providers are unavailable, the graph enters input-required state and alerts the executive.
* **Token Budget Exhaustion**: Per-role budget caps prevent any single agent from consuming disproportionate resources. At 100% budget consumption, the graph pauses and requests human budget approval during the next standup.

---

## Deployment Architecture

### Development Environment (Docker Compose)

Local development uses Docker Compose with profiles for selective service startup:

* PostgreSQL 16 (checkpoint store)
* Redis 7 (circuit breakers, rate-limit state)
* LiteLLM Proxy (with provider registry)
* vLLM (optional, conditional on `LOCAL_GPU_ENABLED=true`)
* DSH Agent Runtime containers (mounted with `profiles/` configuration)
* Dashboard (React dev server)

### Production Environment (Kubernetes with Helm)

Production deployment uses Kubernetes with Helm charts providing:

* Horizontal Pod Autoscaler (HPA) for DSH engineer agent pools (scale based on ticket queue depth)
* StatefulSets for PostgreSQL and Redis with persistent volumes
* Ingress with TLS termination for the authenticated dashboard
* GPU nodeSelector for optional vLLM deployment
* Health checks, restart policies, and resource limits for all services
* Rolling deployments for zero-downtime updates

---

## End-to-End System Integration and Deployment Blueprint

Deploying this autonomous software engineering enterprise involves connecting the following modular components:

1. **State Orchestration Layer**: Deploy LangGraph backed by PostgreSQL and Redis for state-graph management, node transitions, fan-out/fan-in parallel execution, and thread checkpoint persistence. Configure for 13 agent roles with expanded state schema.
2. **Inference and Resilience Tier**: Deploy LiteLLM Proxy with the scalable Provider Registry. Configure `providers.yaml` with available cloud providers (Gemini, Claude, GPT-4o, Groq, OpenRouter). Optionally enable local vLLM tier if GPU is available. Set per-role token budgets for all 13 roles. Configure Redis-backed circuit breakers.
3. **DSH Agent Execution Tier**: Deploy DeepSeek Harness runtime instances for all 13 specialist agents. Mount role-specific `cordis.yml` profiles declaring LiteLLM model routing, `dsh-mcp` tool connections, `dsh-a2a` agent cards, sandbox parameters, and trajectory output destinations.
4. **Agent Routing Layer**: Deploy Agent Router with domain-tag classification rules to dispatch tasks between architect and engineering pools.
5. **Automated Demo Engine**: Deploy Playwright automation services within the demo container. Configure user journey templates for the expense tracker reference application. Enable video capture with visible cursor indicators.
6. **Authenticated Standup Dashboard**: Deploy React dashboard with OAuth2/OIDC authentication (Google, GitHub SSO). Configure SSE bridge for real-time state streaming and DSH trajectory exploration. Set up role-based access control (executive, viewer, admin).
7. **Video Standup Bot**: Deploy Meet or Teams bot based on organization preference. Configure calendar API credentials, bot service account, and feedback transcription pipeline.
8. **Production Deployment**: Deploy to Kubernetes using Helm charts with HPA scaling for DSH agent pods, TLS ingress for dashboard, persistent volumes for PostgreSQL/Redis, and optional GPU node affinity for vLLM.

---

## Works Cited

1. MetaGPT: Meta Programming for A Multi-Agent Collaborative, https://www.alphaxiv.org/abs/2308.00352
2. TensorOpsAI/agent-scrum: Multi-agent simulation platform, https://github.com/TensorOpsAI/agent-scrum
3. ChatDev Framework: Multi-Agent Software Dev, https://www.emergentmind.com/topics/chatdev-framework
4. OpenHands vs SWE-Agent (2026): SWE-bench Scores Compared, https://localaimaster.com/blog/openhands-vs-swe-agent
5. DeepSeek Harness (dsh) Documentation & Architecture, https://github.com/deepseek-ai/deepseek-harness
6. Learn System Design for AI Agents, https://www.freecodecamp.org/news/learn-system-design-for-ai-agents-build-a-production-ready-multi-agent-pr-reviewer/
7. agent-browser - Claude Skill, https://aiagentskills.net/skill/magentosh-skills-agent-browser
8. Amazon Nova Act: Building Reliable Browser Agents, https://caylent.com/blog/amazon-nova-act-building-reliable-browser-agents
9. Building a Real-Time Multi-Agent UI with AG-UI, https://devblogs.microsoft.com/agent-framework/ag-ui-multi-agent-workflow-demo/
10. Announcing the Agent2Agent Protocol (A2A), https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/
11. Scalable BDD Test Automation Using Playwright and Python Behave, https://medium.com/@sowmyamoturu/scalable-bdd-test-automation-using-playwright-and-python-behave-5429cf9490b3
12. MCP vs A2A: Key Differences, Use Cases, and Enterprise Integration, https://www.truefoundry.com/blog/mcp-vs-a2a
13. What is A2A protocol (Agent2Agent)? - IBM, https://www.ibm.com/think/topics/agent2agent-protocol
14. Run Free LLMs at Scale: LiteLLM Gateway, https://stevescargall.com/blog/2026/04/run-free-llms-at-scale-litellm-gateway-with-groq-nvidia-nim-openrouter-and-local-vllm/
15. How to Build LangGraph Multi Agent Systems with Shared Files, https://fast.io/resources/langgraph-multi-agent/
16. What Is Multi-Agent Orchestration? A Complete Guide, https://www.truefoundry.com/blog/what-is-multi-agent-orchestration
17. Systems That Never Stop - Fault-Tolerant AI Agents, https://www.autolearningagents.com/fault-tolerant-ai/
18. Google's Agent-to-Agent (A2A) and Anthropic's Model Context Protocol, https://www.gravitee.io/blog/googles-agent-to-agent-a2a-and-anthropics-model-context-protocol-mcp
19. smolvm - PyPI, https://pypi.org/project/smolvm/0.0.6/
20. LiteLLM Budget Control: Reduce AI and LLM Costs, https://www.almtoolbox.com/blog/litellm-budget-control-reduce-ai-costs/
21. Making the AI Gateway Resilient to Redis Failures, https://docs.litellm.ai/blog/redis-circuit-breaker
22. DeepSeek Harness: Composable AI Agent Infrastructure, https://deepseek.com/blog/deepseek-harness-cordis
23. Implementing resilience patterns with Amazon Bedrock, https://aws.amazon.com/blogs/machine-learning/implementing-resilience-patterns-with-amazon-bedrock-and-llm-gateway/
24. What Is a Fallback Strategy for LLM APIs in 2026?, https://futureagi.com/blog/what-is-llm-fallback-strategy-2026/
25. Rate Limiting in AI Gateway: The Ultimate Guide, https://www.truefoundry.com/blog/rate-limiting-in-llm-gateway
