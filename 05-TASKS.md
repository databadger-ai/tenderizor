# Engineering Task Backlog

This is the implementation-ready task markup. Importers may parse the task ID, phase, priority, size and dependency columns. Checkboxes are the authoritative planning status in this document until tasks are moved into the team’s issue tracker.

## Task conventions

- Priority: P0 launch blocker, P1 required for target release, P2 later improvement.
- Size: XS less than 1 day, S 1–2 days, M 3–5 days, L 6–10 days. Split anything larger than L before implementation.
- Dependencies list task IDs; dash means none.
- A task is not Done until code, tests, documentation, observability and rollback notes satisfy the shared Definition of Done.

## Phase 0 — Charter, baseline, and proof

| Done | ID | Pri | Size | Depends | Deliverable and acceptance |
|---|---|---:|---:|---|---|
| - [ ] | TND-000 | P0 | M | — | Measure current tender workflow on a representative sample; publish stage-by-stage active/cycle time, defect and rework baseline with analyst sign-off |
| - [ ] | TND-001 | P0 | M | — | Build a stratified, bilingual golden corpus covering categories, missing fields, amendments, hard eligibility, pricing and adverse documents; dual-review labels |
| - [ ] | TND-002 | P0 | S | — | Approve federal/non-federal source scope, construction exclusion, language handling and source-access policy |
| - [ ] | TND-003 | P0 | S | — | Approve persona, role, separation-of-duties and approval matrix |
| - [ ] | TND-004 | P0 | M | TND-002 | Complete data-rights, privacy, model-provider, residency, retention and threat-model decision log |
| - [ ] | TND-005 | P0 | L | TND-003 | POC Temporal tender workflow with typed start/update/query, human wait, stale approval rejection, restart and cancellation |
| - [ ] | TND-006 | P0 | M | TND-005 | POC DBOS alternative against the same scenarios and document operational trade-offs |
| - [ ] | TND-007 | P0 | L | TND-001 | POC PydanticAI typed task/output, one capability, one hook, one read tool, usage limits and event translation |
| - [ ] | TND-008 | P0 | M | TND-005,TND-007 | Demonstrate three-lane fan-out/fan-in, partial failure and persisted synthesis |
| - [ ] | TND-009 | P0 | M | TND-000 | Pre-register the 10x pilot protocol, guardrails, sample-size method and sign-off owner |
| - [ ] | TND-010 | P0 | M | TND-000,TND-003 | Prototype opportunity list, evidence viewer, compliance blocker and approval card; usability review with analysts |
| - [ ] | TND-011 | P0 | S | TND-004,TND-005,TND-006,TND-007 | Record workflow-engine, provider and deployment ADRs; revise plan/estimate and obtain sponsor gate |

## Phase 1 — Platform foundation

| Done | ID | Pri | Size | Depends | Deliverable and acceptance |
|---|---|---:|---:|---|---|
| - [ ] | TND-100 | P0 | M | TND-011 | Scaffold tender capability, backend modules, frontend feature, worker entrypoints and compose overlay without a second product shell |
| - [ ] | TND-101 | P0 | L | TND-011 | Publish versioned Pydantic contracts and JSON Schemas for workflow, task, finding, citation, approval and event envelopes |
| - [ ] | TND-102 | P0 | L | TND-101 | Create PostgreSQL schemas, Alembic migrations, service roles and repository ports; migration upgrade/downgrade tests pass |
| - [ ] | TND-103 | P0 | M | TND-101 | Configure S3/MinIO content-addressed storage, versioning and immutable manifest model; hash round-trip tests pass |
| - [ ] | TND-104 | P0 | L | TND-003,TND-100 | Integrate OIDC user context, tenant isolation, RBAC and separation of duties; negative tests pass |
| - [ ] | TND-105 | P0 | M | TND-101 | Implement workflow-event projection and resumable SSE with stable event IDs and terminal error semantics |
| - [ ] | TND-106 | P0 | M | TND-005,TND-100 | Package Temporal client/workers, task queues, health/readiness and local development service |
| - [ ] | TND-107 | P0 | M | TND-004,TND-100 | Add secret-manager interface, safe configuration and egress allowlists; secret scanning passes |
| - [ ] | TND-108 | P0 | M | TND-100 | Add OTel traces, metrics and structured logs with required safe context; validate trace correlation |
| - [ ] | TND-109 | P0 | M | TND-100,TND-102,TND-103,TND-106 | Build Docker images and compose smoke test from fresh clone; services run non-root and health checks pass |
| - [ ] | TND-110 | P0 | M | TND-101,TND-109 | Add CI targets for lint, mypy, unit, contract, integration, frontend, image and compose checks |

## Phase 2 — Sources, documents, and evidence

| Done | ID | Pri | Size | Depends | Deliverable and acceptance |
|---|---|---:|---:|---|---|
| - [ ] | TND-200 | P0 | L | TND-102,TND-103 | Implement official open/new/complete tender adapter with idempotent cursor/snapshot handling and strict category policy |
| - [ ] | TND-201 | P0 | M | TND-200 | Reconcile source counts, cadence and freshness; alert on unexpected gaps without fabricating missing records |
| - [ ] | TND-202 | P0 | M | TND-200 | Add award and contract-history adapters covering the PRD field catalogue, solicitation/contract linking and match-confidence status |
| - [ ] | TND-203 | P0 | L | TND-103,TND-200 | Implement authorized attachment/document retrieval, access-state model, hashes and source manifest |
| - [ ] | TND-204 | P0 | M | TND-203 | Add file-type verification, size limits, malware scan, archive limits and quarantine workflow |
| - [ ] | TND-205 | P0 | L | TND-204 | Parse PDF, DOCX, XLSX, HTML and images; preserve page/sheet/cell/section locators and parser versions |
| - [ ] | TND-206 | P0 | M | TND-205 | Add OCR fallback, quality threshold and manual-review state |
| - [ ] | TND-207 | P0 | M | TND-205 | Implement language detection, original-language preservation and unofficial-translation labelling |
| - [ ] | TND-208 | P0 | L | TND-205 | Implement citation registry and locator resolver; invalid citations cannot satisfy material fields |
| - [ ] | TND-209 | P0 | L | TND-200,TND-208 | Implement every opportunity field in the PRD catalogue with Published/Calculated/Estimated/Inferred/Translated/Unknown/Conflicting/Not-applicable states |
| - [ ] | TND-210 | P0 | L | TND-203,TND-205,TND-208 | Implement notice/document version comparison and typed amendment impact |
| - [ ] | TND-211 | P0 | L | TND-210 | Build dependency invalidation for findings, scores, costs, drafts and approvals; golden amendment tests pass |
| - [ ] | TND-212 | P0 | L | TND-102 | Build versioned company capability/evidence profile with owners, expiry, entities and verification |
| - [ ] | TND-213 | P1 | M | TND-209 | Add PostgreSQL FTS/pgvector search projection, rebuild command and saved views |

## Phase 3 — PydanticAI and durable analysis

| Done | ID | Pri | Size | Depends | Deliverable and acceptance |
|---|---|---:|---:|---|---|
| - [ ] | TND-300 | P0 | L | TND-007,TND-101,TND-106 | Implement PydanticAI runtime adapter using full event streaming/iteration and stable application events |
| - [ ] | TND-301 | P0 | L | TND-300 | Implement agent registry, typed dependencies, immutable definitions and adaptive model policy |
| - [ ] | TND-302 | P0 | L | TND-301 | Implement versioned skill/capability registry, stable IDs, on-demand loading and rollback pointer |
| - [ ] | TND-303 | P0 | L | TND-302,TND-104 | Implement filtered toolsets and always-on context, prompt-boundary, authorization, provenance, privacy, budget and audit hooks |
| - [ ] | TND-304 | P0 | M | TND-303 | Implement tenant/provider rate limiter, task/model/tool/token/time/CAD-cost budgets and circuit breaker |
| - [ ] | TND-305 | P0 | M | TND-301 | Implement AG-01 Discovery Analyst with golden evaluation |
| - [ ] | TND-306 | P0 | L | TND-301,TND-208,TND-210 | Implement AG-02 Evidence and Amendment Analyst with citation/invalidation tests |
| - [ ] | TND-307 | P0 | L | TND-301,TND-212 | Implement AG-03 Compliance and AG-04 Supplier-Fit Analysts with hard-gate schemas |
| - [ ] | TND-308 | P1 | M | TND-202,TND-301 | Implement AG-05 Market and Award Analyst with ambiguous-match review |
| - [ ] | TND-309 | P1 | M | TND-301 | Implement AG-07 Contract/Clarification Analyst with external-send prohibition |
| - [ ] | TND-310 | P0 | M | TND-301,TND-303 | Implement AG-09 independent Red-Team Reviewer and authorship-independence gate |
| - [ ] | TND-311 | P0 | L | TND-305,TND-306,TND-307,TND-310 | Implement AG-00 Supervisor typed plan, Temporal fan-out/fan-in, conflict preservation and proposed transition |
| - [ ] | TND-312 | P0 | L | TND-311 | Implement workflow states through bid/no-bid, approvals, deadlines, cancellation and amendment return |
| - [ ] | TND-313 | P0 | M | TND-300,TND-311 | Enforce structured ERROR then terminal completion, no silent runtime/model fallback, and partial-result preservation |
| - [ ] | TND-314 | P0 | L | TND-001,TND-300 | Build deterministic agent tests and Pydantic Evals datasets with cost/latency/quality reports |
| - [ ] | TND-315 | P1 | L | TND-304,TND-311,TND-314 | Raise concurrency from 3 to 6, then test ceiling 10; document backpressure, provider limits, cost and incremental quality |

## Phase 4 — UI and approvals

| Done | ID | Pri | Size | Depends | Deliverable and acceptance |
|---|---|---:|---:|---|---|
| - [ ] | TND-400 | P0 | L | TND-100,TND-200 | Build work inbox, tender list, saved filters, freshness, deadline risk and assignments |
| - [ ] | TND-401 | P0 | L | TND-209 | Build tender workspace Overview and Evidence tabs with source/status/version controls |
| - [ ] | TND-402 | P0 | L | TND-208,TND-401 | Build split evidence viewer with citation navigation, corrections and review status |
| - [ ] | TND-403 | P0 | L | TND-307,TND-312 | Build requirements/compliance matrix with blocker states, owners and evidence |
| - [ ] | TND-404 | P0 | M | TND-210,TND-211 | Build amendment timeline/diff and invalidated-artifact view |
| - [ ] | TND-405 | P0 | L | TND-104,TND-312 | Build approval inbox with expected revision, role, separation of duties, expiry, reason and audit |
| - [ ] | TND-406 | P0 | L | TND-105,TND-311 | Build agent/workflow timeline with tasks, tools, status, retries, tokens, cost and failures |
| - [ ] | TND-407 | P1 | M | TND-400,TND-405 | Add comments, notifications, ownership and escalation rules |
| - [ ] | TND-408 | P0 | M | TND-400,TND-406 | Accessibility, keyboard, responsive and empty/error/loading-state pass |
| - [ ] | TND-409 | P0 | L | TND-400,TND-408 | Playwright E2E for analyst and super-user workflows plus negative RBAC and reconnect |

## Phase 5 — Commercial and bid workspace

| Done | ID | Pri | Size | Depends | Deliverable and acceptance |
|---|---|---:|---:|---|---|
| - [ ] | TND-500 | P0 | L | TND-307,TND-308 | Implement hard-gate-first opportunity scoring, configurable weights and explanation |
| - [ ] | TND-501 | P0 | L | TND-102 | Implement Decimal/currency/unit/tax cost engine and reusable goods/services templates |
| - [ ] | TND-502 | P0 | L | TND-501 | Add low/base/high scenarios, contingency, cash need, markup, margin, floor and sensitivity |
| - [ ] | TND-503 | P1 | M | TND-308,TND-502 | Implement evidence-adjusted comparable and price-to-win workspace without implying losing-bid data |
| - [ ] | TND-504 | P0 | M | TND-301,TND-501,TND-502 | Implement AG-06 Commercial Analyst; it proposes but cannot approve price |
| - [ ] | TND-505 | P0 | M | TND-405,TND-502 | Implement commercial approval threshold and stale-calculation invalidation |
| - [ ] | TND-506 | P0 | L | TND-307,TND-309 | Implement response-plan generator from compliance matrix and approved evidence |
| - [ ] | TND-507 | P0 | L | TND-301,TND-506 | Implement AG-08 Bid Strategy/Drafting Analyst with unsupported-placeholder controls |
| - [ ] | TND-508 | P0 | L | TND-310,TND-507 | Implement independent technical/commercial/compliance review and disposition workflow |
| - [ ] | TND-509 | P0 | L | TND-211,TND-405,TND-508 | Implement package freeze, manifest, requested-form reconciliation, hashes and manual-submission checklist |
| - [ ] | TND-510 | P0 | M | TND-509 | Implement human entry/verification of submission receipt; no portal credentials or submission API |
| - [ ] | TND-511 | P1 | L | TND-202,TND-500,TND-510 | Implement outcome/debrief/award/contract/amendment linkage and reviewed learning dataset |

## Phase 6 — Hardening, pilot, and launch

| Done | ID | Pri | Size | Depends | Deliverable and acceptance |
|---|---|---:|---:|---|---|
| - [ ] | TND-600 | P0 | L | TND-303,TND-409 | Execute prompt injection, malicious file, SSRF, tenant isolation, secret leakage and unauthorized-tool suite |
| - [ ] | TND-601 | P0 | L | TND-312,TND-509 | Execute restart, duplicate, timeout, retry, cancellation, stale approval, source outage and amendment chaos tests |
| - [ ] | TND-602 | P0 | M | TND-102,TND-103,TND-106 | Prove database/object/workflow backup, point-in-time restore and disaster recovery |
| - [ ] | TND-603 | P0 | L | TND-315,TND-406 | Load/cost test 100 active tender workflows and 6–10 logical lanes with backpressure |
| - [ ] | TND-604 | P0 | M | TND-108,TND-603 | Build production dashboards/alerts and verify every critical incident is diagnosable by correlation ID |
| - [ ] | TND-605 | P0 | M | TND-600,TND-601,TND-602 | Write and exercise source outage, model outage, reprocessing, security incident, kill-switch, rollback and restore runbooks |
| - [ ] | TND-606 | P0 | L | TND-001,TND-314,TND-509 | Run full frozen-corpus release evaluation and disposition every critical defect |
| - [ ] | TND-607 | P0 | L | TND-606 | Shadow-run a live cohort without external action; audit citation, requirement, amendment, cost and latency outcomes |
| - [ ] | TND-608 | P0 | L | TND-009,TND-607 | Run controlled user pilot and 10x/non-inferiority analysis including corrections and rework |
| - [ ] | TND-609 | P0 | M | TND-605,TND-608 | Conduct production-readiness review with product, procurement, commercial, security/privacy, QA and engineering sign-off |
| - [ ] | TND-610 | P1 | M | TND-609 | Canary rollout with pinned definitions, kill switch, rollback window and daily quality/cost review |

## Explicitly deferred tasks

| Done | ID | Pri | Size | Depends | Deliverable and acceptance |
|---|---|---:|---:|---|---|
| - [ ] | TND-700 | P2 | L | TND-609 | Add one approved broader-public-sector portal adapter with legal/access review and contract tests |
| - [ ] | TND-701 | P2 | L | TND-609 | Evaluate OpenSearch only from measured PostgreSQL search limits |
| - [ ] | TND-702 | P2 | L | TND-609 | Add ERP/CRM supplier and realized-margin integrations with tenant/privacy controls |
| - [ ] | TND-703 | P2 | L | TND-609 | Threat-model future isolated submission gateway; requires documented portal permission and two-person approval |

TND-703 is design-only until separately authorized. It does not authorize implementation or use.

## Definition of Ready

A task is Ready when:

- scope, owner and dependency versions are known;
- applicable PRD requirement and ADR are linked;
- security/privacy/data classification is known;
- input/output schemas and source-of-truth are identified;
- acceptance tests, failure cases, observability and rollback are specified;
- required fixture/corpus access is approved;
- no unresolved product decision would materially change implementation.

## Definition of Done

A task is Done when:

- code follows existing architecture and has no temporary or redundant production path;
- Pydantic/TypeScript types cover public boundaries;
- structured logs/traces/metrics are present and safe;
- unit, property, contract and relevant integration tests pass;
- negative/error/retry/idempotency behavior is tested;
- documentation and migrations are updated;
- Docker build/runtime sanity passes where applicable;
- frontend work passes browser E2E and accessibility checks;
- golden/evaluation regression passes for AI behavior;
- security review is complete for trust-boundary changes;
- rollback or disable mechanism is proven;
- reviewer independent of author accepts the task.

## Proposed verification commands

These targets should be added during implementation and made runnable from the repository root:

~~~bash
make check
make contracts
make platform-test
make tenders-lint
make tenders-typecheck
make tenders-test
make tenders-contract-test
make tenders-eval
make tenders-build
make tenders-compose-check
make tenders-e2e
make tenders-security-test
make tenders-pilot-report
~~~

Until those targets exist, teams must record the exact uv, pytest, Ruff, mypy, npm, Playwright and Docker Compose commands in each task/PR.
