# QA and Acceptance Matrix

## 1. Quality strategy

Quality is evaluated across five independent dimensions:

1. Source integrity — did the system ingest and version the authoritative material correctly?
2. Deterministic correctness — do schemas, calculations, rules, state transitions and permissions behave exactly?
3. AI quality — are extractions and recommendations supported, complete, calibrated and useful?
4. Workflow reliability — do retries, restarts, approvals, amendments and partial failures preserve correct state?
5. Human outcome — does the tool reduce work without degrading bid quality?

No aggregate score may compensate for a critical compliance, security, stale-amendment, authorization or submission failure.

## 2. PRD traceability

| Requirement | Primary tests | Release evidence |
|---|---|---|
| FR-01 Sources | Adapter contract, count reconciliation, cadence/outage, idempotency | Source reconciliation report |
| FR-02 Evidence | Hash, immutability, version, retrieval, object restore | Evidence integrity report |
| FR-03 Dossier | Pydantic validation, field-state, conflict, identifier fixtures | Golden extraction report |
| FR-04 Documents | Parser/OCR/file/security matrix, locator resolution | Format coverage report |
| FR-05 Amendments | Semantic diff, dependency invalidation, stale approval/package | Amendment gate report |
| FR-06 Company profile | Evidence ownership, expiry, entity scope, tenant/RBAC | Company evidence audit |
| FR-07 Compliance | Critical-requirement recall, hard gate, reviewer corrections | Compliance release report |
| FR-08 Commercial | Decimal/property/reconciliation/sensitivity tests | Commercial control report |
| FR-09 Multi-agent | Typed contract, fan-out/join, budget, failure, cancellation, no recursion | Agent orchestration report |
| FR-10 Skills/hooks | Versioning, allowlist, on-demand load, rollback, always-on policy | Definition compatibility report |
| FR-11 HITL | Auth, role, expected revision, expiry, separation, audit, revocation | Approval control report |
| FR-12 Draft/package | Evidence coverage, placeholders, cross-document consistency, manifest | Package readiness report |
| FR-13 Outcome learning | Match confidence, correction, reviewed-only dataset | Learning lineage report |
| FR-14 Search/export | Filters, tenant scope, rebuild, source-linked export | Search/export test report |

## 3. Golden corpus

### Composition

The release corpus must be stratified across:

- Goods, Services, Services Related to Goods, and mixed-category review cases.
- Federal buyers and representative procurement instruments.
- English, French and bilingual notices/documents.
- Native-text, scanned, table-heavy and spreadsheet-heavy documents.
- Single and multiple amendment histories.
- Complete, missing, conflicting and inaccessible information.
- Security, Controlled Goods, licences, bonding, Indigenous set-aside, Canadian-content and other tender-specific conditions.
- Lowest-price, combined-score, rated and budget-constrained evaluation methods.
- Goods and services pricing schedules, options, ceilings and no-guarantee arrangements.
- Competitive notices, ACAN, standing offers and supply arrangements.
- Award/contract matches, ambiguous matches and unmatched records.
- Benign and adversarial prompt-like instructions embedded in documents.

### Ground truth

- Two independent reviewers label every critical requirement and material field.
- Disagreements are adjudicated by the procurement SME and retained in the decision log.
- Each label includes the exact source version and locator.
- Corpus changes create a new immutable version.
- Training examples and release-test examples remain separated.

## 4. Source and data tests

- Official record-count reconciliation by dataset and scope.
- Duplicate and out-of-order delivery.
- Reference-number change with stable solicitation number.
- Multi-category construction exclusion.
- Missing, null, zero and currency semantics.
- SAP/other-source delay and stale-feed alert.
- Access blocked, account required, paid portal and broken link.
- Re-download with unchanged and changed hashes.
- Unsupported, corrupt, encrypted, oversized and malicious files.
- Parser/OCR fallback and locator round trip.
- Object-store/database restore and search-index rebuild.
- Contract-history multiple rows/amendments and ambiguous matching.

## 5. Deterministic domain tests

### Schemas and contracts

- Required fields and extra-field policy.
- Backward/forward compatibility for additive optional fields.
- Unknown event type handling.
- Malformed event rejection before persistence.
- JSON Schema and generated client compatibility.

### Compliance

- Fail and fatal Unknown block progression.
- Remediable items require owner and due date.
- Published requirements remain separate from assumptions/risks.
- Expired company evidence cannot satisfy a requirement.
- Human correction is versioned and invalidates dependent output.

### Commercial

- Decimal-only money math.
- Currency and tax treatment.
- Unit/quantity/duration/options.
- Markup versus gross margin.
- Landed cost and service-loaded cost.
- Low/base/high and sensitivity.
- Floor versus price-to-win conflict.
- No price approval when required inputs are missing or stale.

Use property-based tests for arithmetic invariants and round-trip serialization.

## 6. AI evaluation

### Extraction

- Precision, recall and F1 by field.
- Citation locator validity.
- Citation entailment.
- Published/calculated/estimated/inferred/translated/unknown classification.
- Cross-language consistency.
- Missing-information honesty.

### Compliance and reasoning

- Critical mandatory requirement recall.
- False-eligible and false-fail rates.
- Evidence sufficiency.
- Correct separation of mandatory, rated, acceptance, contractual and readiness items.
- Contradiction detection.
- Confidence calibration and abstention.

### Drafting and review

- Requirement coverage.
- Unsupported claim count and severity.
- Placeholder visibility.
- Figure/date/name consistency.
- Amendment currency.
- Independent reviewer defect recall.
- Human acceptance/correction effort.

### Evaluation controls

- Deterministic evaluators first.
- LLM judges only with a published rubric, pinned model and sampled human verification.
- Store model, prompt, skill, tool and dataset versions.
- Repeat evaluations to detect variance.
- Report cost, latency and quality together.

## 7. Multi-agent tests

- Supervisor activates only required roles.
- Specialists cannot delegate.
- Task depth remains one.
- Per-tender, per-tenant and global ceilings.
- Shared usage and cost accounting.
- One lane failure with other lanes succeeding.
- Required versus optional lane failure.
- Conflicting findings preserved through synthesis.
- Supervisor retry reuses persisted findings.
- Cancellation after amendment.
- Six-lane and ten-lane backpressure.
- Provider rate-limit recovery.
- No double tool execution after retry/replay.
- Stable agent/capability/toolset IDs across compatible workflow replay.

Acceptance:

- Ten logical lanes can be scheduled without losing, duplicating or misattributing results.
- Production concurrency is promoted from 3 to 6 and then up to 10 only when cost, rate-limit, quality and resilience gates pass.

## 8. Workflow and HITL tests

- Start, query, update, signal, cancel and resume.
- API restart, worker restart and workflow-worker replacement.
- Timer and deadline across restart.
- Duplicate command/update and idempotency.
- Approval with correct/incorrect role.
- Self-approval and separation-of-duties denial.
- Approval against stale revision/hash.
- Approval expiry and revocation.
- Amendment arriving before, during and after approval.
- Retry policy does not multiply provider/tool attempts unexpectedly.
- Event handler replay remains idempotent.
- Terminal failures persist visible ERROR then completion state.
- Global kill switch pauses new AI work while evidence remains accessible.

## 9. Security and adversarial tests

### Identity and authorization

- missing/expired token;
- role escalation;
- cross-tenant object reference;
- approval replay;
- direct activity/tool invocation;
- admin attempting bid approval without business role;
- stale client history forging approval.

### Content and tools

- prompt injection in notice, PDF, spreadsheet cell, OCR image and supplier attachment;
- malicious link and SSRF target;
- file polyglot, archive bomb and malware;
- tool-name collision and capability-ID manipulation;
- unapproved MCP server/tool;
- tool arguments outside evidence/tenant scope;
- model response requesting secrets or external action.

### Data leakage

- secrets absent from logs/traces/workflow payloads;
- pricing, resumes and security material excluded from default telemetry;
- object links expire and cannot cross tenant;
- model/provider payload adheres to approved data classification;
- exports honor role and legal hold.

Any cross-tenant exposure, secret leak or unauthorized state change is a release blocker.

## 10. Browser and usability tests

Playwright paths:

1. Analyst discovers, opens and corrects a tender dossier.
2. Analyst traces a field to source and marks a conflict.
3. Compliance lead reviews hard blockers and requests clarification.
4. Bid manager records bid/no-bid.
5. Commercial lead builds and approves a scenario.
6. Draft owner completes response sections.
7. Independent reviewer returns defects and verifies rework.
8. Authorized user freezes package and records manual receipt.
9. Amendment invalidates prior approval and prevents stale export.
10. Unauthorized user cannot view, edit, approve or export another tenant/role’s data.
11. Browser loses/reconnects SSE without losing timeline.
12. Super-user inspects audit, model cost and agent failure.

Accessibility:

- keyboard-only critical flows;
- visible focus and logical order;
- labels and error association;
- color-independent status;
- screen-reader names;
- zoom/responsive operation;
- WCAG 2.2 AA target for production.

## 11. Performance, load, and cost tests

Workloads:

- official feed refresh;
- 100 active tender workflows;
- 10,000 searchable notices/awards;
- 6–10 logical specialist lanes per high-priority tender;
- large documents and spreadsheet schedules;
- amendment burst near deadlines;
- approval inbox burst.

Measure:

- API p50/p95/p99;
- ingestion and dossier completion;
- workflow queue/schedule latency;
- model/tool latency and failure;
- first persisted progress event;
- tokens and CAD/USD cost per lane/tender/submitted package;
- database/object/search utilization;
- retry amplification and rate-limit time;
- memory/CPU by worker family.

Backpressure must keep the API responsive and preserve deadline priority.

## 12. Reliability and recovery tests

- stop/restart API during active workflows;
- kill model activity worker;
- lose database connection;
- object store temporary outage;
- Temporal unavailable and restored;
- model provider outage/rate limit;
- partial source outage;
- duplicate webhook/feed;
- deploy workflow code with in-flight executions;
- point-in-time database restore;
- object version restore;
- search projection rebuild;
- global AI disable and prior-version rollback.

Record RPO/RTO evidence. A successful health check alone is not recovery proof.

## 13. The 10x experiment

### Hypothesis

The assisted workflow produces at least ten times more independently accepted qualified dossiers per analyst-FTE week, without worse quality.

### Design

- Pre-register sample, strata, tasks, metrics, exclusion rules and analysis.
- Use a randomized crossover: analysts complete comparable cases with manual and assisted workflows.
- Include reading, corrections, review, rework, abandoned cases and waiting attributable to the tool.
- Blind independent reviewers to workflow where practical.
- Report median, distribution and confidence intervals; do not report only the best cases.
- Run a live shadow cohort after historical evaluation.

### Primary outcomes

- accepted qualified dossiers per analyst-FTE week;
- active analyst minutes per accepted dossier;
- active human minutes per independently accepted package;
- amendment-to-approved-impact time.

### Quality guardrails

- 100 percent material citation coverage;
- 100 percent critical deadline/amendment/mandatory requirement capture on launch corpus;
- at least 98 percent audited factual-field accuracy;
- zero false eligible caused by a missed critical criterion;
- zero stale approved packages;
- zero late or unauthorized submissions;
- reviewer acceptance non-inferior to manual baseline;
- approved unit cost.

The claim fails if throughput improves but any critical guardrail regresses.

## 14. Phase release gates

| Gate | Required evidence | Approvers |
|---|---|---|
| QG-0 Architecture | Baseline, corpus, POC, threat model, ADRs | Sponsor, engineering, procurement |
| QG-1 Source truth | Reconciliation, idempotency, recovery, tenant tests | Engineering, QA |
| QG-2 Evidence | Citation, parser, amendment, injection reports | Procurement SME, QA, security |
| QG-3 AI/HITL | Agent evaluation, hard-gate, retry, approval audit | Procurement, engineering, security |
| QG-4 Bid workspace | Commercial property tests, draft evidence, stale export | Commercial, compliance, bid manager |
| QG-5 Pilot | Security, resilience, restore, 10x, unit economics | All accountable owners |

## 15. No-go conditions

Do not launch when any of these is true:

- unsupported material facts are displayed as published;
- a critical requirement or amendment is missed in the release corpus;
- a false Eligible result comes from a missed fatal condition;
- stale approval/package can survive material source change;
- any role can self-authorize or forge client-side approval;
- AI can access buyer communication or submission capability;
- cross-tenant data, secrets or confidential content leaks;
- workflow state or evidence is lost on tested restart/recovery;
- cost, latency or retry behavior is unbounded;
- browser users cannot trace, correct and review outputs;
- backup/restore, incident, kill switch and rollback are unproven.

## 16. Required CI and release artifacts

Each release stores:

- source adapter reconciliation;
- schema compatibility;
- unit/property/contract/integration results;
- workflow replay and chaos results;
- golden AI evaluation;
- security/adversarial results;
- browser E2E and accessibility results;
- image/SBOM/vulnerability/signature results;
- performance/cost report;
- backup/restore evidence;
- unresolved risk disposition;
- named approvals and rollback target.
