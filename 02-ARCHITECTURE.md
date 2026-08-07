# Target Architecture

## 1. Architecture recommendation

Adopt a durable, supervised agent architecture with four explicit planes:

1. Experience plane — React workbench and FastAPI BFF.
2. Control plane — Temporal tender workflows, approvals, timers, retries, cancellation, and fan-out/fan-in.
3. Intelligence plane — PydanticAI supervisor and specialist agents using typed dependencies, outputs, capabilities, toolsets, and hooks.
4. Evidence plane — PostgreSQL business state, immutable object storage, search indexes, citations, audit events, and company evidence.

PydanticAI is the agent runtime, not the workflow engine, authorization system, database, or submission bot. Temporal owns durable control flow. Deterministic services own source ingestion, parsing, formulas, status transitions, and side effects.

## 2. Architectural principles

| ID | Principle |
|---|---|
| ARC-01 | Verel owns public contracts, state, permissions, events, and side effects; PydanticAI remains replaceable |
| ARC-02 | One durable workflow per tender/bid lifecycle |
| ARC-03 | One microservice per domain/failure boundary, never one per AI agent |
| ARC-04 | Strict Pydantic contracts at every API, event, workflow, tool, and agent boundary |
| ARC-05 | Deterministic code first; use an LLM only for language-heavy ambiguity |
| ARC-06 | The current source package and amendments are authoritative |
| ARC-07 | Every derived artifact is traceable to immutable evidence and definition versions |
| ARC-08 | Human approval pauses workflow state; it is not a client-supplied Boolean |
| ARC-09 | The supervisor alone may delegate; depth is one and total concurrent specialists is capped at ten |
| ARC-10 | All source text is untrusted input and cannot modify system policy |
| ARC-11 | Deploy read-only first and keep a global automation kill switch |
| ARC-12 | Every retryable activity is idempotent and every terminal failure is visible |

## 3. System context

~~~mermaid
flowchart LR
    Team["Trading and bid team"] --> UI["Tender Assistant workbench"]
    Admin["Administrator / auditor"] --> UI
    UI --> Platform["Verel tender capability"]

    Platform --> CB["CanadaBuys official datasets and notices"]
    Platform --> Portals["Approved downstream procurement portals"]
    Platform --> Company["Company, supplier, ERP and CRM evidence"]
    Platform --> Models["Approved model providers"]
    Platform --> Notify["Approved notification channels"]

    Human["Named approver"] --> Platform
    Platform -. "draft package only" .-> Submit["External bid submission channel"]
    Human --> Submit
~~~

The dotted path is intentional: the system prepares and records the package, while an authorized human performs submission unless a future, formally approved integration exists.

## 4. Container view

~~~mermaid
flowchart TB
    Browser["React / TypeScript workbench"]
    API["FastAPI BFF and domain API"]
    Temporal["Temporal service"]
    Ingest["Source ingestion workers"]
    Docs["Document intelligence workers"]
    Agents["PydanticAI workflow workers"]
    Notify["Notification and export workers"]
    DB["PostgreSQL business store"]
    Obj["S3-compatible immutable object store"]
    Search["PostgreSQL FTS + pgvector"]
    OTel["OpenTelemetry collector and backend"]
    Sources["Official feeds and approved portals"]
    LLM["Approved model providers"]

    Browser <--> API
    API <--> Temporal
    API <--> DB
    API --> Obj
    API --> Search

    Sources --> Ingest
    Ingest --> Temporal
    Ingest --> DB
    Ingest --> Obj

    Temporal <--> Docs
    Temporal <--> Agents
    Temporal <--> Notify
    Docs --> Obj
    Docs --> DB
    Docs --> Search
    Agents --> LLM
    Agents --> DB
    Agents --> Obj
    Notify --> DB

    API --> OTel
    Ingest --> OTel
    Docs --> OTel
    Agents --> OTel
    Notify --> OTel
~~~

## 5. Deployable service boundaries

### 5.1 Web and API

Responsibilities:

- authentication, authorization, tenant and role enforcement;
- tender queries, command validation, approval endpoints, exports, and SSE;
- server-owned UI state and workflow projections;
- never execute long-running AI work in an HTTP request.

Recommended implementation:

- existing Verel React/Vite shell and UI primitives;
- FastAPI with strict Pydantic request/response models;
- existing Verel capability and route gating;
- stable event translator rather than exposing PydanticAI-native events directly.

### 5.2 Source ingestion workers

Responsibilities:

- poll and reconcile official datasets and subscriptions;
- idempotently upsert notice metadata;
- retrieve only permitted documents;
- hash, virus-scan, classify, and store raw evidence;
- start or signal the appropriate Temporal workflow;
- detect amendments and source-access failures.

This service is deterministic. It may use a lightweight model only for exceptional document classification after deterministic checks fail.

### 5.3 Document intelligence workers

Responsibilities:

- parse PDF, DOCX, XLSX, HTML, image and archive inputs;
- OCR when native text is inadequate;
- preserve page, table, sheet, cell, section and paragraph locators;
- segment documents, detect language, and build searchable representations;
- compare versions and generate structured amendment diffs.

Parsers run in a constrained environment. Suspicious or unsupported content is quarantined rather than passed to an LLM.

### 5.4 PydanticAI workflow workers

Responsibilities:

- host the supervisor and specialist agent registry;
- execute typed agent tasks inside Temporal activities/workflows;
- compose versioned skills/capabilities and filtered toolsets;
- translate model/tool events into the stable application event contract;
- enforce per-tender and per-tenant token, request, tool, time, cost, and concurrency budgets;
- persist findings, evidence references, conflicts, limitations, and usage.

These workers scale horizontally by Temporal task queue. Agent roles are modules/configurations inside the worker image, not network services.

### 5.5 Notification and export workers

Responsibilities:

- deliver in-app/email notifications from approved templates;
- create source-linked dossier and bid-package exports;
- record delivery attempts and receipts;
- never send buyer communications without a separately authorized future integration.

### 5.6 Infrastructure services

- PostgreSQL: authoritative business and audit state.
- Object storage: immutable raw files and versioned generated artifacts.
- Temporal: durable workflow history and task queues, with its own supported persistence.
- OpenTelemetry: traces, metrics and logs.
- Optional search service: add OpenSearch only after measured PostgreSQL search limits.

## 6. Why Temporal

The lifecycle can last days or weeks, waits on people, reacts to amendments, has strict deadlines, and must resume after failure. Temporal provides durable workflows, activities, child workflows, timers, signals, updates, queries, retries, and versioning. PydanticAI has an official Temporal durability capability, but an agent becomes durable only when its run executes inside a Temporal workflow.

Recommended ownership:

- Workflow code owns states, transitions, timeouts, deadlines, agent fan-out, joins, approvals and cancellation.
- Activities own model requests, tool calls, document work and external I/O.
- Temporal Updates accept authenticated state-changing human decisions.
- Temporal Queries provide current workflow state to the API.
- Business artifacts remain in the application database/object store; workflow payloads contain small typed references.

Temporal is not the business database and its history is not the user-facing audit ledger.

## 7. Tender workflow

~~~mermaid
stateDiagram-v2
    [*] --> Discovered
    Discovered --> EvidencePending
    EvidencePending --> EvidenceReady
    EvidenceReady --> ParallelAnalysis
    ParallelAnalysis --> AnalysisReview
    AnalysisReview --> ClarificationPending: blocking unknown
    ClarificationPending --> ParallelAnalysis: answer or amendment
    AnalysisReview --> NoBid: fatal fail or human decision
    AnalysisReview --> BidDecisionPending: eligible
    BidDecisionPending --> NoBid: rejected
    BidDecisionPending --> CommercialAnalysis: approved
    CommercialAnalysis --> PricingApproval
    PricingApproval --> Drafting: approved
    PricingApproval --> NoBid: rejected
    Drafting --> IndependentReview
    IndependentReview --> Rework: defects
    Rework --> Drafting
    IndependentReview --> SubmissionApproval: pass
    SubmissionApproval --> PackageReady: approved
    SubmissionApproval --> Rework: rejected
    PackageReady --> Submitted: human records receipt
    Submitted --> Awarded
    Submitted --> Lost
    Submitted --> Cancelled
    Awarded --> ContractDelivery
    ContractDelivery --> Closed
    NoBid --> Closed
    Lost --> Closed
    Cancelled --> Closed
~~~

Any material amendment can transition an active state back to EvidencePending and revoke dependent approvals.

## 8. Parallel agent execution

### 8.1 Fan-out policy

The supervisor constructs a typed plan from deterministic workflow context. Temporal starts only the specialists whose prerequisites and capabilities are satisfied.

- Phase 0 ceiling: 3 simultaneous specialist runs per tender.
- Pilot ceiling after promotion gate: 6 simultaneous specialist runs per tender.
- Upper capability limit after quality, cost, provider-rate and resilience gates: 10.
- Delegation depth: 1.
- Specialists cannot spawn specialists.
- Global and tenant provider limits apply in addition to the per-tender ceiling.
- A failure in one lane does not discard completed lanes.
- Required lanes fail closed; optional lanes may complete with explicit Unavailable status.

### 8.2 Fan-in policy

The supervisor receives versioned AgentFinding objects rather than full conversations. It:

- checks schema and evidence coverage;
- identifies conflicts and missing required lanes;
- preserves dissent instead of averaging it away;
- requests deterministic recalculation where possible;
- creates human review tasks for unresolved material conflicts;
- emits a synthesis referencing original findings.

PydanticAI shared usage accounting and UsageLimits should protect individual runs; system-wide rate limiting remains an infrastructure concern.

## 9. Typed contracts

The following contracts must be versioned and published as JSON Schema:

### TenderWorkflowInput

- api_version
- tenant_id
- tender_id
- solicitation_number
- source_snapshot_ids
- company_profile_version
- workflow_definition_version
- agent/skill/model policy versions
- deadline and time zone
- requested lanes
- time/token/tool/cost/concurrency budgets

### AgentTask

- api_version
- workflow_id, task_id, parent_task_id
- tender_id, correlation_id, causation_id
- source_agent and target_role
- task_type and objective
- artifact_refs and evidence_scope
- allowed_capabilities and denied_tools
- expected_output_schema
- deadline, priority, budget, attempt and idempotency_key

### AgentFinding

- task_id, status and recommendation
- structured result
- evidence_refs with source/document hash and locator
- confidence band and rationale
- missing facts, assumptions, conflicts and limitations
- published-versus-inferred classification
- human_review_required and reason
- definition/model/tool versions
- usage, latency and cost

### ApprovalRequest

- approval_id, type, required_role and separation-of-duties rule
- workflow/tender/artifact identifiers
- artifact hashes and source snapshot set
- decision options
- risk summary and expiring_at
- previous approvals invalidated

### WorkflowEvent

- api_version
- event_id, type, occurred_at
- tenant, tender, workflow, task, agent and correlation identifiers
- safe payload
- sequence number
- source and definition versions
- terminal and retryable flags

Unknown event types and additive optional fields must be tolerated at adapters; malformed required envelopes fail validation before persistence.

## 10. Evidence and data architecture

### 10.1 Storage authority

| Data | Authority |
|---|---|
| Raw notices and documents | Content-addressed object storage |
| Normalized tender and business records | PostgreSQL |
| Citations and extraction lineage | PostgreSQL |
| Search index and embeddings | Rebuildable PostgreSQL FTS/pgvector projection |
| Workflow control state | Temporal |
| User-facing workflow projection | PostgreSQL projection |
| Agent/model/tool telemetry | OTel backend plus safe usage records |
| Prompt, agent, skill and workflow definitions | Git for executable code; immutable published records for runtime configuration |

### 10.2 Database isolation

Use one managed PostgreSQL cluster initially with separate databases or schemas and service-specific credentials:

- tender_domain
- identity_and_approval
- workflow_projection
- audit_and_usage
- search_projection

No service writes directly to another service’s tables. Cross-service changes use typed commands, workflow activities, or a transactional outbox.

### 10.3 Evidence lineage

Every derived value links through:

Derived artifact → extraction/finding → citation → document version → content hash → source snapshot → retrieval metadata.

An amendment creates a new document version; it never mutates the prior source. A dependency index determines which findings, calculations, drafts and approvals become stale.

## 11. Human-in-the-loop control

PydanticAI deferred tool approval is useful for pausing a run, but it is not an authorization boundary. Browser history and client approval flags are untrusted.

For each approval:

1. API authenticates the actor.
2. API checks tenant, role, separation of duties and current revision.
3. API sends a typed Temporal Update.
4. Workflow validator confirms expected state, artifact hash, source versions and expiry.
5. Decision is appended to the business audit ledger.
6. Sensitive activity rechecks authorization and approval receipt.
7. Workflow advances or returns to rework.

Approval types:

- eligibility/compliance interpretation;
- clarification wording;
- bid/no-bid;
- pricing and contingency;
- unsupported exception or contractual deviation;
- response freeze;
- final submission package;
- receipt recording and post-award corrections.

## 12. Skills, tools, MCP and hooks

- Skills are versioned PydanticAI capabilities containing trusted instructions and optionally toolsets/hooks.
- Long-tail skills use on-demand loading with stable IDs.
- Toolsets are filtered server-side by role, tenant, workflow state and source scope.
- MCP is an integration protocol, not an authorization layer.
- Mutating tools remain absent until the workflow is in an authorized state.
- Always-on security/evidence/privacy/budget hooks cannot be deferred or disabled by a skill.
- Stable agent names, capability IDs and toolset IDs are compatibility contracts for durable workflows.

See [Agents, skills, and hooks](03-AGENTS-SKILLS-HOOKS.md).

## 13. API and UI event path

PydanticAI-native events remain internal. Workers map them to versioned WorkflowEvent records and a user-facing projection.

~~~mermaid
sequenceDiagram
    participant U as User
    participant UI as React UI
    participant API as FastAPI
    participant T as Temporal
    participant W as PydanticAI Worker
    participant DB as Event Projection

    U->>UI: Start or review tender
    UI->>API: Authenticated command
    API->>T: Start / Update workflow
    T->>W: Scheduled activity
    W->>DB: Persist safe progress event
    DB-->>API: Projection update
    API-->>UI: SSE event
    UI-->>U: Timeline, evidence, status
    U->>UI: Approve / reject
    UI->>API: Decision with expected revision
    API->>T: Validated Update
    T->>DB: Approval outcome projection
    API-->>UI: New state
~~~

If SSE disconnects, the browser resumes from the last event ID. It never reconstructs authority from local chat history.

## 14. Security architecture

- OIDC and short-lived tokens.
- User context propagated explicitly; no ambient service-account impersonation.
- Role and capability filtering before tools reach the model.
- Separate read and mutation credentials.
- Egress allowlists for source and model workers.
- Private object storage and pre-signed short-lived download links.
- Antivirus/content disarm policy for uploaded or retrieved files.
- Prompt-injection guards before model context assembly and before every tool call.
- Encryption at rest and in transit.
- Approved secret manager; no secret values in workflow payloads.
- Full pricing, resumes, security documents and model content excluded from telemetry by default.
- Audit records append-only with integrity protection and controlled correction events.
- Model provider contractual review for retention, training, region and incident handling.

## 15. Observability contract

Required structured context:

- timestamp, level, environment, service and version;
- tenant_id, user_id when safe, correlation_id;
- tender_id, workflow_id, task_id and attempt;
- agent name/version, skill IDs/versions, tool ID/version;
- source snapshot and artifact hashes;
- model/provider, requests, tokens, cost and latency;
- state transition, approval ID, outcome and error class.

Required dashboards:

- source freshness and reconciliation;
- workflow state distribution and deadline risk;
- worker/task-queue saturation and retries;
- agent and tool latency/error/cost;
- approval backlog and age;
- amendment invalidation backlog;
- citation coverage and human correction;
- quality-evaluation drift;
- backup/restore and dependency health.

Errors include safe structured stack traces. One actionable event is preferred to many uncorrelated log lines.

## 16. Docker and deployment topology

### Local and integration

Create a compose.tenders.yaml overlay containing:

- web/API using the existing Verel image;
- tender ingestion worker;
- document worker;
- PydanticAI/Temporal worker;
- notification/export worker;
- PostgreSQL;
- MinIO;
- Temporal development service and UI;
- OTel collector and a lightweight local backend.

Do not use an archived Temporal Docker Compose repository as a production template. Use current Temporal samples for development and choose Temporal Cloud or an explicitly operated cluster for production.

### Production

Recommended initial topology:

- API and worker containers on ECS/Fargate or Kubernetes;
- managed PostgreSQL with PITR;
- managed object storage with versioning and lifecycle rules;
- Temporal Cloud, or a separately approved self-hosted Temporal cluster;
- managed OIDC and secret manager;
- managed OTel-compatible observability;
- private networking, controlled egress and WAF at the public edge.

The specific cloud and region remain sponsor decisions.

## 17. Repository integration

Target layout when implementation is authorized:

~~~text
platform/
  backend/src/verel_platform/
    tenders/
      api/
      domain/
      application/
      adapters/
      agents/
      skills/
      workflows/
      approvals/
      observability/
  frontend/src/
    features/tenders/
  workers/
    tenders/
  compose.tenders.yaml
core/packages/verel-core-contracts/
  ...shared workflow and event contracts only
~~~

Add tender intelligence as a capability/preset over the existing kernel. Do not reintroduce a second frontend shell, product-specific branching, or a parallel authentication system.

## 18. Technology decisions and alternatives

| Concern | Recommendation | Alternative | Decision rationale |
|---|---|---|---|
| Agent runtime | PydanticAI 2.x | OpenAI Agents SDK | User requirement, typed dependencies/outputs, capabilities, hooks, toolsets, MCP, official durability integrations |
| Durable workflow | Temporal | DBOS; Prefect | Temporal best fits long-lived approval-heavy business workflows and separate worker scaling |
| API | Existing FastAPI | Django/DRF | Existing platform fit and Pydantic contract alignment |
| UI | Existing React/Vite | New standalone app | Preserves one shell and capability model |
| Business store | PostgreSQL | Existing MySQL | Strong JSON/search/vector ecosystem and natural fit for durable domain/audit workloads; validate operational ownership |
| Raw artifacts | S3/MinIO | Database blobs | Immutability, versioning, scale and content-addressed storage |
| Search MVP | PostgreSQL FTS + pgvector | OpenSearch | Lower operational burden; extract OpenSearch only after measured need |
| Messaging | Temporal task queues + outbox | Kafka/NATS | Avoid a second distributed control plane until throughput or integration needs prove it |
| Observability | Existing OTel/Langfuse-compatible stack | Logfire-only | PydanticAI emits OTel and Verel already has OTel integration |

### Temporal versus DBOS

DBOS is a credible lower-operations alternative because it runs in process and checkpoints to PostgreSQL. It is attractive for a smaller team and should remain the fallback in the POC. Temporal is recommended because independent worker pools, long waits, message-driven human decisions, workflow visibility, and deployment/versioning are central requirements here.

## 19. Failure modes and degradation

| Failure | Required behavior |
|---|---|
| CanadaBuys feed unavailable | Retain last known snapshot, mark freshness stale, retry with backoff, alert after SLO |
| Attachment inaccessible | Mark Access blocked, continue non-dependent lanes, open human task |
| Parser/OCR failure | Quarantine file, preserve original, retry bounded alternatives, require review |
| Model/provider outage | Pause affected activities, use approved fallback only if contract-tested, never silently change model policy |
| One specialist fails | Preserve successful results; retry safely; block join only if lane required |
| Worker/API restart | Workflow resumes without duplicate findings or lost approvals |
| Amendment during drafting | Cancel or obsolete affected tasks, invalidate artifacts/approvals, return to evidence state |
| Approval arrives against stale artifact | Reject update with current revision and reason |
| Tool attempts unauthorized action | Fail closed, emit security event, do not expose tool to model next step |
| Budget exceeded | Stop further agent work, persist partial results, request human decision |
| UI/SSE disconnect | Resume from persisted event cursor |
| Database unavailable | Stop writes, avoid external actions, recover from durable workflow/activity retry |

## 20. Architecture fitness functions

- Domain modules cannot import model-provider SDKs.
- Tool execution requires a typed user/workflow context.
- Mutating tools require an approval policy and idempotency key.
- Every material AgentFinding has at least one valid citation or an explicit Unknown status.
- Specialist agents have no delegation tool.
- Workflow definitions enforce agent and budget ceilings.
- No PydanticAI event crosses the public API unversioned.
- No approval can survive a material artifact/source version change.
- No raw external document text can enter system instructions.
- Docker images run as non-root and pass dependency/image scans.

## 21. Promethean analysis

The frontier element is the 6–10-agent parallel team. The bold move is not to make those agents autonomous; it is to treat them as typed, replaceable analytical workers inside a deterministic procurement workflow. This departs from chat-centric agent products and should produce better auditability and recoverability.

The cost of boldness is higher orchestration, evaluation and observability work. Ten agents can multiply cost, latency, disagreement and failure surface. The architecture therefore caps fan-out, activates roles only when useful, forbids recursive delegation, and requires a controlled pilot to prove that each specialist adds value.

## 22. Athena Head self-critique

### Challenge

The user requested microservices, but a new product with uncertain load can be damaged by premature service fragmentation.

### Reinforcement

The proposal uses coarse-grained service families aligned to distinct scale, security and failure boundaries, while keeping domain logic modular and agent roles in one worker family. The POC may begin with fewer process boundaries, but contracts and task queues preserve later extraction.

### Weakest joint

Temporal adds meaningful operating and workflow-versioning complexity. Confidence depends on a Phase 0 proof that approval waits, streaming projections, amendment cancellation, replay, and ten-way fan-out can be implemented and operated by the actual team. DBOS remains the documented fallback if that proof fails.

### Verdict

Pass with reinforcement: proceed only through the Phase 0 workflow-engine gate.
