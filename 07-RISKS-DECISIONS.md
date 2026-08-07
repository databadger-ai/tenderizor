# Risks and Architecture Decisions

## 1. Proposed architecture decisions

These decisions are Proposed until accepted through the Phase 0 gate.

| ADR | Decision | Status | Consequence |
|---|---|---|---|
| ADR-TND-001 | Add tender intelligence as a Verel capability/preset, not a product fork | Proposed | Reuses one kernel/UI/auth; must respect existing contracts |
| ADR-TND-002 | Use PydanticAI 2.x only behind Verel-owned typed runtime/task/event contracts | Proposed | Gains typed agent features without framework-owned business policy |
| ADR-TND-003 | Use Temporal for durable tender workflows, subject to POC; DBOS is fallback | Proposed | Strong durability/HITL at meaningful operational cost |
| ADR-TND-004 | Use coarse-grained services; agents are logical roles in worker pools | Proposed | Independent scaling without ten service deployments |
| ADR-TND-005 | PostgreSQL is authoritative for tender/business/audit state | Proposed | Adds/standardizes an operational store; requires ownership and migration plan |
| ADR-TND-006 | S3-compatible object storage is authoritative for raw and generated artifacts | Proposed | Immutable/versioned evidence outside relational blobs |
| ADR-TND-007 | PostgreSQL FTS/pgvector is the initial search projection | Proposed | Low operations; OpenSearch remains an extraction path |
| ADR-TND-008 | Temporal task queues plus transactional outbox; no Kafka/Redis requirement in MVP | Proposed | Fewer distributed systems; revisit with measured demand |
| ADR-TND-009 | Ten agent roles, adaptive 6–10 logical lanes, concurrency promoted 3 → 6 → max 10 | Proposed | Satisfies parallelism goal while containing cost/failure |
| ADR-TND-010 | Human submission only in MVP | Proposed | Limits automation but avoids unauthorized irreversible actions |
| ADR-TND-011 | Published skills/prompts/workflows are immutable and version-pinned | Proposed | Safer replay/rollback; higher configuration discipline |
| ADR-TND-012 | Existing Verel event vocabulary remains public; PydanticAI events stay internal | Proposed | Frontend/history compatibility at translation cost |
| ADR-TND-013 | Read-only and draft-only is the default; external tools absent, not prompt-discouraged | Proposed | Strong safety boundary |
| ADR-TND-014 | Model provider is selected by policy and conformance, not hard-coded in agents | Proposed | Portability; requires provider-specific testing |
| ADR-TND-015 | 10x is a measured pilot gate with quality non-inferiority | Proposed | Prevents ungrounded productivity claim |

## 2. Tool selection

### 2.1 Durable workflow candidates

| Dimension | Temporal | DBOS | Prefect |
|---|---|---|---|
| Fit | Excellent for long-lived, message-driven, approval-heavy workflows | Strong for Python/Postgres-centered durability | Strong for data/automation flows |
| Operating model | Separate service/cloud plus workers | In-process library plus system database | Server/cloud plus workers |
| HITL/message flow | Queries, Signals, Updates, durable waits | Durable workflows/queues; validate full approval UX in POC | Paused/suspended interactive flows |
| Worker isolation/scale | Mature task queues and independent workers | Simpler, fewer moving parts | Strong orchestration, data-oriented |
| PydanticAI integration | Official capability | Official capability | Official capability |
| Lock-in/exit | Workflow history/version semantics create meaningful exit cost | Python decorators and DB state create moderate exit cost | Flow/task semantics create moderate exit cost |
| Main cost | Operational and workflow-versioning complexity | Younger operational surface and process coupling | Less natural fit for long-lived bid state machine |
| Verdict | Recommended, conditional on POC | Preferred fallback for smaller operational team | Consider for ingestion/data pipelines, not primary bid lifecycle |

### 2.2 Service granularity

| Option | Benefit | Cost | Verdict |
|---|---|---|---|
| One service per agent | Independent scaling and ownership in theory | Network/state/operations explosion; wrong boundaries before evidence | Reject |
| Modular monolith only | Fastest initial development | Weak isolation for OCR, ingestion and AI worker scaling | Suitable only for POC |
| Coarse-grained service families | Scales distinct workloads and security boundaries while retaining coherent domains | Requires contracts and distributed operations | Recommend |

### 2.3 Search

| Option | Benefit | Cost | Verdict |
|---|---|---|---|
| PostgreSQL FTS + pgvector | Fewer systems, transactions and easy rebuild | May hit relevance/scale limits later | MVP recommendation |
| OpenSearch | Strong search, facets and hybrid scale | Cluster cost and operational burden | Add only after measured trigger |

## 3. Risk register

Likelihood and impact use Low, Medium, High. A High-impact risk cannot be accepted implicitly.

| ID | Risk | Likelihood | Impact | Prevention/mitigation | Trigger/owner |
|---|---|---|---|---|---|
| R-01 | 10x premise is not achievable on end-to-end work | Medium | High | Baseline first; optimize bottleneck stages; report guarded throughput | Phase 0 results / Product sponsor |
| R-02 | More agents add cost/disagreement without quality | High | High | Adaptive activation, depth 1, budgets, incremental-value evaluation, promote concurrency in gates | Cost/quality regression / AI lead |
| R-03 | Missed mandatory criterion causes false Eligible | Medium | Critical | Dual-reviewed corpus, deterministic hard gate, cited requirement matrix, human compliance approval | Any critical miss / Compliance lead |
| R-04 | Amendment leaves stale analysis or package | Medium | Critical | Immutable versions, dependency graph, cancellation, automatic revocation, stale-export test | Material diff / Bid manager |
| R-05 | AI invents official fact or company capability | Medium | Critical | Explicit field states, citation requirement, verified company evidence, fail closed | Unsupported material claim / Product |
| R-06 | Prompt injection changes tool/workflow behavior | High | Critical | Untrusted-data boundary, filtered tools, egress, deterministic policy hooks, adversarial suite | Policy/tool violation / Security |
| R-07 | Client forges HITL approval | Medium | Critical | Server auth/RBAC, Temporal Update validation, expected revision/hash, tool recheck | Approval mismatch / Security |
| R-08 | Sensitive bid/company/personnel data reaches logs/model | Medium | Critical | Classification, minimization, approved endpoints, redaction, telemetry off by default | DLP/trace finding / Privacy |
| R-09 | CanadaBuys/downstream access changes | High | High | Official feed adapters, source contracts, freshness/reconciliation, human access state | Count/freshness anomaly / Data owner |
| R-10 | HTML/portal automation violates access expectations | Medium | High | No crawler foundation, legal/access review, manual submission | New adapter proposal / Legal-product |
| R-11 | Temporal complexity exceeds team capacity | Medium | High | POC, training, Cloud option, runbooks, DBOS fallback | POC/ops fail / Engineering lead |
| R-12 | Workflow code change breaks replay | Medium | High | Stable IDs, versioning, replay tests, pinned in-flight definitions | Replay failure / Workflow lead |
| R-13 | Layered retries duplicate model/tool/external effects | Medium | High | One retry owner, idempotency keys, receipts, retry-budget tests | Duplicate or amplified calls / SRE |
| R-14 | Cost/rate limits block deadline-critical work | Medium | High | Deadline priority, provider quotas, backpressure, budget escalation, fallback policy | Queue/cost alert / SRE-bid manager |
| R-15 | Award/history matching creates misleading intelligence | Medium | Medium | Match confidence, manual review, source/value semantics | Low-confidence match / Market analyst |
| R-16 | Pricing model produces wrong margin or currency | Medium | Critical | Decimal property tests, approved reference data, scenario review, commercial approval | Reconciliation fail / Commercial lead |
| R-17 | Microservice fragmentation slows delivery | Medium | High | Coarse service families, one codebase/image families, extraction criteria | Cross-service churn / Architect |
| R-18 | Search technology underperforms | Low initially | Medium | Measure relevance/latency; rebuildable projection; OpenSearch trigger | p95/relevance SLO / Platform |
| R-19 | Human approval backlog erases speed benefit | High | High | Exception-first UI, deadlines/escalation, batch only low-risk reviews, staffing metrics | Approval-age SLO / Bid manager |
| R-20 | Users over-trust confidence/ranking | Medium | High | Evidence-first UI, no false precision, explanations, uncertainty and training | Override/error pattern / Product |
| R-21 | Bilingual translation changes legal meaning | Medium | High | Preserve original, mark unofficial, cite original, human review when material | Language conflict / Compliance |
| R-22 | Local Docker stack is mistaken for production architecture | Medium | High | Explicit production ADR, managed dependencies, security and DR gates | Deployment request / Platform |
| R-23 | Vendor/model lock-in | Medium | Medium | Verel contracts, model policy, golden conformance, portable artifacts/OTel | Provider change / AI lead |
| R-24 | Contract/copyright restrictions on attachments | Medium | High | Rights metadata, internal access controls, no unauthorized redistribution | Export/source issue / Legal-product |

## 4. Risk acceptance rules

- Critical risks require prevention evidence and named executive/security/compliance acceptance; they cannot be accepted by the engineering team alone.
- A risk mitigation implemented only in a prompt is not a control.
- A fallback model/provider must pass the same contract, safety and quality suite before activation.
- Repeated critical source/AI defects pause affected automation and start root-cause investigation.
- Work may continue in read-only evidence mode while higher-risk capabilities are disabled.

## 5. Effort and cost uncertainty

Indicative estimate:

| Work | Person-weeks |
|---|---:|
| Discovery, baseline, architecture POC | 10–14 |
| Platform/contracts/security foundation | 13–18 |
| Sources/documents/evidence | 15–21 |
| Durable workflows/agents/evaluation | 16–22 |
| UI/HITL | 12–17 |
| Commercial/drafting/package | 15–21 |
| Hardening/pilot | 14–20 |
| Total before overlap | 95–133 |
| Expected with parallel work/reuse | 75–105 |

Estimate caveats:

- External portal access, model/provider decisions and company-evidence quality can dominate schedule.
- Existing Verel components reduce implementation but add integration/compatibility tests.
- Ten-agent concurrency increases evaluation and operational work more than linearly.
- Submission integration is excluded.

## 6. Rollout and rollback

### Feature controls

- tender capability enablement;
- source adapter enablement;
- per-agent/skill version;
- maximum logical/concurrent lanes;
- model/provider policy;
- drafting and commercial modules;
- all AI execution global kill switch;
- all external-action tools permanently off in MVP.

### Rollback triggers

- critical unsupported fact;
- missed mandatory requirement or amendment;
- stale approved/exported package;
- unauthorized or cross-tenant action/data;
- secret or confidential data leak;
- non-idempotent duplicate;
- workflow replay/recovery failure;
- unbounded cost/retry;
- quality non-inferiority failure.

### Recovery order

1. Disable affected agent/skill/source or global AI.
2. Preserve raw evidence and audit events.
3. Pin last known good definitions.
4. Identify affected artifacts by lineage.
5. Recompute/review derived artifacts.
6. Record correction, cause and disposition.
7. Re-enable through shadow/canary gates.

## 7. Self-critique

### Hardest challenge

The design could still be too ambitious for an initial product: durable workflows, new evidence stores, ten agent roles, document processing, pricing and a full bid workspace are several products’ worth of surface.

### Resolution

The plan sequences a narrow read-only vertical slice and makes every expansion phase-gated. Agent roles are configurations, not services, and the MVP can ship value after evidence/compliance even if commercial/drafting phases are delayed.

### Weakest joint

The actual manual baseline and organization’s capability data do not yet exist in this package. They determine whether 10x is feasible and whether ranking/compliance can be accurate. TND-000, TND-001 and TND-212 are therefore product blockers, not administrative setup.

### Verdict

Pass with reinforcement. Authorize Phase 0 only; approve later phases after evidence.
