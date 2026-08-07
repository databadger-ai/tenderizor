# Phased Action Plan

## 1. Delivery strategy

Deliver a sequence of production-shaped vertical slices. Every phase has an explicit exit gate and rollback boundary. Do not start autonomous external actions; the final production pilot remains read-only/draft-only with human submission.

Indicative schedule: 14–18 calendar weeks with the team described in README. Estimates assume the existing Verel API, React shell, auth patterns, event contracts, Docker build, and observability foundations are reused.

## 2. Workstreams

| Workstream | Scope |
|---|---|
| Product and procurement | Workflow, company profile, golden corpus, acceptance, operating procedures |
| Platform and contracts | Typed schemas, capability integration, identity, RBAC, audit, storage |
| Source and evidence | CanadaBuys adapters, documents, OCR, citations, amendments, search |
| Durable workflow | Temporal POC, lifecycle, fan-out/fan-in, approvals, retries, timers |
| AI runtime | PydanticAI agents, skills, hooks, toolsets, budgets, evaluation |
| Commercial and bid | Scoring, comparables, costing, pricing, drafting, review, package |
| UI/UX | Inbox, pipeline, tender workspace, evidence, matrix, approvals, activity |
| Quality and operations | CI, golden tests, security, load, resilience, backup, incident, pilot |

## 3. Phase plan

### Phase 0 — Charter, baseline, and architecture proof

Duration: 2 weeks\
Effort: 10–14 person-weeks\
Risk: High; this phase validates the business premise and weakest architectural joint.

Deliverables:

- sponsor-approved MVP scope and authority matrix;
- measured manual workflow baseline;
- stratified bilingual golden tender corpus;
- data-rights, privacy and model-provider decision log;
- Temporal versus DBOS proof covering restart, approval wait, amendment cancellation, typed fan-out/fan-in, event projection and idempotency;
- PydanticAI spike with typed outputs, one skill, one hook, one read-only toolset and stable event translation;
- minimal clickable UI workflow or low-fidelity prototype;
- revised estimate and unit-economics budget.

Exit gate:

- source scope and company-profile owner approved;
- baseline and corpus frozen;
- Temporal POC survives worker/API restart and stale approval;
- required live progress can be projected to UI;
- no external action capability exists;
- team accepts operational burden or formally selects DBOS fallback;
- sponsor approves the 10x experiment design.

Rollback:

- discard the POC branch/environment; retain evidence, corpus, measurements and ADRs.

### Phase 1 — Platform foundation and read-only ingestion

Duration: 2–3 weeks\
Effort: 13–18 person-weeks

Deliverables:

- tender capability scaffold in Verel;
- versioned cross-service/task/event contracts;
- PostgreSQL schemas/migrations and immutable object storage;
- OIDC/RBAC context and tenant isolation;
- official CanadaBuys open/new/complete/award/contract adapters;
- source reconciliation, raw snapshotting, hashes and data-quality alerts;
- Docker Compose integration and OTel baseline;
- opportunity list and source-freshness UI.

Exit gate:

- record counts reconcile to the approved official scope;
- repeated ingestion is idempotent;
- source outage and malformed record tests pass;
- all raw inputs are recoverable by hash;
- no user can cross tenant boundaries;
- local compose and CI checks are reproducible from a fresh clone.

Rollback:

- disable tender capability manifest and workers; retain immutable source snapshots.

### Phase 2 — Evidence, documents, and amendment control

Duration: 3 weeks\
Effort: 15–21 person-weeks

Deliverables:

- document inventory and authorized retrieval;
- malware/type checks, parsers and OCR;
- bilingual source preservation and unofficial translation labels;
- citation/locator model and evidence viewer;
- normalized tender dossier;
- semantic amendment diff and dependency invalidation;
- company capability/evidence profile;
- search and saved views.

Exit gate:

- material-field citation coverage at least 95 percent on the golden corpus;
- every attachment is versioned or explicitly inaccessible;
- amendment golden tests detect every material change;
- changed source versions revoke affected analysis and approval state;
- prompt-injection documents cannot modify system/tool policy.

Rollback:

- revert derived extraction versions and rebuild from immutable raw evidence.

### Phase 3 — Durable supervised AI analysis

Duration: 3 weeks\
Effort: 16–22 person-weeks

Deliverables:

- PydanticAI runtime behind stable Verel contracts;
- ten role definitions and adaptive activation;
- versioned skill/capability registry and filtered toolsets;
- always-on authorization, evidence, budget, privacy, event and audit hooks;
- Temporal workflow with discovery, evidence, parallel analysis, review and human gates;
- compliance, supplier-fit, award-intelligence and clarification agents;
- independent red-team agent;
- per-run/provider/tenant budgets and circuit breakers;
- transparent agent timeline.

Parallelism rollout:

1. POC ceiling 3 concurrent model runs.
2. Pilot ceiling 6 after cost, rate-limit and failure tests.
3. Hard ceiling 10 only after the six-agent gate passes.

The system still executes 6–10 logical specialist lanes asynchronously; the runtime may apply backpressure rather than issue all model requests at the same instant.

Exit gate:

- all inter-agent contracts validate;
- zero critical mandatory-requirement misses on release corpus;
- required lanes fail closed and optional lanes fail visibly;
- ten-lane workflow survives partial failure, cancellation and restart;
- no recursive delegation;
- 100 percent approval audit coverage;
- no silent model/runtime fallback.

Rollback:

- route workflow to deterministic/read-only analysis and disable individual agents/skills by version.

### Phase 4 — Minimal transparent UI and HITL operations

Duration: 2–3 weeks, overlapping Phase 3\
Effort: 12–17 person-weeks

Deliverables:

- work inbox and deadline risk;
- pipeline and tender workspace;
- evidence/source viewer;
- compliance matrix and blockers;
- amendment impact page;
- approval inbox with expected-revision control;
- agent run/cost/failure timeline;
- assignments, comments, saved views and audit access;
- accessibility and keyboard-flow validation.

Exit gate:

- an unfamiliar analyst completes a representative workflow without hidden state;
- every AI value exposes evidence and status;
- stale approvals are rejected;
- browser reconnect resumes from persisted event cursor;
- negative RBAC and separation-of-duties E2E tests pass.

Rollback:

- hide tender capability tab and preserve API/audit state for investigation.

### Phase 5 — Commercial, bid, and package workspace

Duration: 3 weeks\
Effort: 15–21 person-weeks

Deliverables:

- hard-gate-first opportunity scoring;
- lawful comparable-award analysis;
- deterministic goods/services cost models;
- low/base/high scenarios, markup, margin and cash exposure;
- commercial approval gate;
- compliance-matrix-driven response plan and drafting;
- independent technical/commercial/compliance red-team review;
- internal package freeze, manifest, hashes and manual-submission checklist;
- award/outcome linkage.

Exit gate:

- arithmetic property tests pass across currency/tax/unit/option cases;
- every draft claim maps to approved evidence or an explicit placeholder;
- no price becomes final without commercial approval;
- a material amendment prevents stale package export;
- package export reconciles every requested form/section and produces hashes;
- external submission remains unavailable.

Rollback:

- disable commercial/drafting capabilities independently; retain read-only tender intelligence.

### Phase 6 — Hardening and controlled pilot

Duration: 2–4 weeks\
Effort: 14–20 person-weeks

Deliverables:

- security/threat-model closure;
- chaos, restart, duplicate-delivery, source-outage and backup/restore tests;
- performance, cost and six-to-ten-lane concurrency evidence;
- incident, recovery, reprocessing, audit and kill-switch runbooks;
- frozen model/prompt/skill/workflow versions;
- shadow-mode live cohort;
- controlled user pilot and 10x comparison;
- production-readiness review and launch decision.

Exit gate:

- every no-go gate in QA document passes;
- restore and rollback are demonstrated;
- no stale/late/unauthorized outcome in pilot;
- quality is non-inferior to the manual baseline;
- unit economics are approved;
- procurement, product, commercial, security/privacy and engineering owners sign off.

Rollback:

- global AI kill switch returns the product to read-only evidence/search;
- pin prior definitions and replay affected derived artifacts;
- retain all audit events and corrections.

## 4. First 30 days

### Week 1

- approve scope, roles, data boundaries and open decisions;
- observe and time the current workflow;
- select 30–50 representative historical/live tenders for corpus design;
- inventory existing Verel seams and deployment constraints;
- create threat model and provider questionnaire.

### Week 2

- freeze corpus v1 and baseline protocol;
- implement Temporal/DBOS comparison spike;
- implement one typed PydanticAI extraction/compliance task;
- demonstrate restart, approval wait, stale update and event projection;
- prototype opportunity list, evidence viewer and approval card.

### Week 3

- decide workflow engine and target deployment;
- finalize contracts and database/evidence model;
- scaffold capability, compose overlay and CI targets;
- implement official open/new tender ingestion and reconciliation.

### Week 4

- store immutable raw snapshots and document manifests;
- ship first end-to-end read-only vertical slice:
  source record → dossier → citation → analyst correction → audit event;
- review actual cycle time, cost and risks; re-estimate remaining phases.

## 5. Milestones

| Milestone | Target | Demonstration |
|---|---|---|
| M0 Architecture gate | End week 2 | Durable POC, baseline, corpus, decisions |
| M1 Source truth | End week 5 | Reconciled official feeds and immutable evidence |
| M2 Evidence control | End week 8 | Source-backed dossier and amendment invalidation |
| M3 Supervised analysis | End week 11 | Typed multi-agent workflow and hard compliance gate |
| M4 Bid workspace | End week 14 | Pricing, drafting, review and package freeze |
| M5 Pilot decision | Weeks 16–18 | Quality, 10x, security, resilience and unit economics |

## 6. Staffing and RACI

| Deliverable | Accountable | Responsible | Consulted |
|---|---|---|---|
| Product scope and success | Product sponsor | Product lead | Trading/bid team |
| Procurement workflow/corpus | Bid manager | Procurement SME, analyst | Compliance, commercial |
| Architecture/contracts | Engineering lead | Backend/AI/platform engineers | Security, product |
| Source/evidence | Engineering lead | Backend/data engineer | Procurement SME |
| Agents/skills/evals | AI lead | AI engineer, QA | Procurement SME |
| Workflow/HITL | Engineering lead | Workflow/backend engineer | Security, bid manager |
| UI | Product lead | Frontend engineer | Analysts, accessibility reviewer |
| Commercial engine | Commercial lead | Backend engineer | Bid manager, finance |
| Security/privacy | Security owner | Platform/security engineer | Legal/privacy |
| Release/pilot | Product sponsor | QA/SRE/product | All approval owners |

## 7. Verification sequence per vertical slice

1. Format and lint.
2. Static type checking.
3. Domain unit and property tests.
4. Contract/schema compatibility tests.
5. Adapter integration tests with recorded official fixtures.
6. Workflow replay, retry, cancellation and idempotency tests.
7. Agent deterministic tests and golden evaluations.
8. API and database integration tests.
9. Frontend unit/component tests.
10. Docker build and compose health.
11. Browser E2E including negative RBAC.
12. Security/adversarial and source-amendment tests.
13. Runtime/log/trace validation.

Green CI is necessary but not sufficient; each phase must satisfy its evidence gate.

## 8. Decision cadence

- Daily engineering risk/blocked review.
- Twice-weekly procurement corpus and error review during Phases 2–5.
- Weekly cost/quality/latency dashboard review.
- Phase gate with named approvers before scope expands.
- Immediate stop and root-cause investigation for unsupported official facts, missed critical criteria, stale approvals/packages, cross-tenant access, secret leakage, or unauthorized action.

## 9. Launch and rollout

1. Historical offline evaluation.
2. Shadow mode on live notices.
3. Internal analyst cohort with no decision automation.
4. Read-only recommendations with mandatory human verification.
5. Draft assistance and package export.
6. Six-agent pilot concurrency after the quality/cost/resilience promotion gate.
7. Ten-agent ceiling only after the second promotion gate and where evaluations prove incremental value.
8. Additional source adapters one at a time.
9. External integrations only through separate ADR, threat model and approval.
