# Product Requirements Document

## 1. Product summary

The CanadaBuys AI Tender Assistant is a supervised workbench for a trading and bid team. It continuously discovers eligible opportunities, assembles source-backed tender dossiers, evaluates eligibility, estimates commercial attractiveness, supports bid/no-bid decisions, drafts compliant response material, and learns from awards and delivered contracts.

The product is workflow-first, not chat-first. Users should see the work, evidence, state transitions, agent activity, exceptions, approvals, and unresolved questions. Chat is an optional way to ask questions about a tender, not the system of record.

## 2. Problem

Analysts currently spend substantial time searching multiple sources, downloading and reading documents, copying fields, comparing amendments, checking mandatory requirements, locating prior awards, calculating costs, coordinating reviewers, and preparing bid packages. The work is repetitive but high-risk: one missed requirement, stale amendment, incorrect assumption, or late submission can invalidate the bid.

The opportunity is to automate repeatable evidence handling and parallelize bounded specialist analysis while retaining human judgment and accountability at every consequential decision.

## 3. Product goals

### G-01 — Increase throughput

Increase qualified opportunities processed per analyst-week by at least 10x during a controlled production pilot, at equal or better quality.

### G-02 — Reduce active work

Reduce median active analyst time for discovery, dossier creation, initial compliance assessment, and compliance-matrix preparation by the targets in Section 14.

### G-03 — Improve responsiveness

Detect and assess new notices and amendments early enough that humans have materially more time for supplier engagement, pricing, strategy, and review.

### G-04 — Improve evidence quality

Make every material claim reviewable from its original notice, amendment, attachment, award record, contract record, or approved company evidence.

### G-05 — Preserve human authority

Automate collection, analysis, drafting, and checking without granting an AI authority to certify facts, accept terms, communicate externally, or submit a bid.

### G-06 — Create a learning loop

Connect opportunities, decisions, bids, awards, contract amendments, delivery outcomes, and realized margins so ranking and estimates improve from reviewed evidence.

## 4. Non-goals

- Replacing procurement, legal, tax, security, or executive accountability.
- Guaranteeing a tender win or guaranteeing a specific margin.
- Scraping every CanadaBuys HTML page.
- Circumventing portal authentication, fees, access prerequisites, robots instructions, or terms.
- Autonomous buyer communication or bid submission.
- Inferring confidential competitor prices or coordinating pricing with competitors.
- Treating historical awards as the range of all submitted offers.
- Creating a separate deployable service for each AI persona.
- Rewriting the rest of Verel as part of this product.

## 5. Users and roles

| Role | Primary needs | Permissions |
|---|---|---|
| Trading analyst | Discover, screen, investigate, compare, ask questions | Read; edit analysis; request reviews |
| Bid manager | Own pipeline, bid/no-bid, assignments, deadlines, package | Approve workflow gates except final price/signature where separated |
| Compliance lead | Verify mandatory/rated criteria and supplier evidence | Approve compliance conclusions; block bid |
| Commercial lead | Build cost model, scenarios, margin, cash exposure | Approve pricing recommendation |
| Technical contributor | Supply technical response and evidence | Edit assigned response sections |
| Executive approver | Authorize bid/no-bid and final submission package | Named high-risk approvals |
| Administrator | Manage users, source adapters, models, agents, skills, retention | Configuration only; cannot self-approve bids by virtue of admin role |
| Auditor | Inspect immutable evidence, decisions, model activity, and receipts | Read-only audit access |

Separation of duties must be configurable. Production defaults prevent the same person from preparing and finally approving pricing or the submission package.

## 6. Product workflow

### Stage 0 — Company readiness

Maintain a versioned capability profile with legal entities, registrations, ownership, products, services, regions, licences, certifications, security status, personnel, manufacturers, suppliers, past performance, insurance, bonding, financial limits, and capacity. Each fact has evidence, owner, validity dates, and verification status.

### Stage 1 — Discovery and ingestion

Ingest official CanadaBuys open/new/complete tender datasets, saved-search notifications, award data, and contract history. Support approved downstream portal adapters later. Reconcile expected record counts and preserve raw source snapshots.

### Stage 2 — Notice and document dossier

Normalize identifiers, buyer entities, dates, categories, languages, status, amendment metadata, links, attachments, and access requirements. Parse documents and create field-level citations without overwriting originals.

### Stage 3 — Amendment control

Detect every notice or attachment change, generate a source-linked diff, identify affected conclusions, invalidate derived artifacts, and reopen required reviews.

### Stage 4 — Relevance screening

Match opportunity subject, region, timing, estimated scale, supplier availability, strategic fit, and capacity. Produce Include, Exclude, or Review with reasons.

### Stage 5 — Eligibility and compliance gate

Evaluate published mandatory and rated criteria separately. Cover registration, jurisdiction, Canadian content, Indigenous set-asides, prequalification, experience, security, Controlled Goods, licences, certifications, insurance, bonding, site visits, samples, personnel, manufacturer authorization, financial capacity, delivery feasibility, and submission mechanics.

Each item is Pass, Remediable, Fail, or Unknown. Fatal Fail and unresolved fatal Unknown states block Bid regardless of ranking score.

### Stage 6 — Clarification

Maintain a register of missing or conflicting information, impact, question deadline, proposed wording, internal approver, official answer, related amendment, and affected artifacts. The system drafts questions but cannot send them.

### Stage 7 — Market and award intelligence

Link comparable tenders, awards, and contract histories. Normalize buyer, supplier, classification, value, currency, dates, duration, options, amendments, selection method, trade agreements, and delivery region. Assign match confidence and route ambiguous matches to review.

### Stage 8 — Commercial model

Calculate fully burdened cost, low/base/high scenarios, cash requirement, contingency, markup, gross margin, internal price floor, and evidence-adjusted price-to-win range. Inputs and formulas are versioned and reviewable.

### Stage 9 — Bid/no-bid decision

Apply the hard gate first, followed by weighted scoring for technical fit, competitive position, risk-adjusted contribution, probability of win, strategic fit, supplier certainty, capacity, and contract/operational risk. Record the human decision and reasons.

### Stage 10 — Response planning and drafting

Create a compliance matrix linking every criterion to evidence, owner, response section, expected score, reviewer, and status. Generate drafts only from approved evidence and clearly mark unsupported placeholders.

### Stage 11 — Independent review

Run technical, compliance, commercial, legal-risk, security/privacy, and adversarial reviews. Reviewers see unresolved evidence gaps and amendment status.

### Stage 12 — Submission readiness

Freeze the approved package, verify forms, signatures, files, pricing reconciliation, amendment currency, channel, identifier, deadline, and time zone. An authorized human performs the external submission and records receipt, response history, timestamps, and hashes.

### Stage 13 — Outcome and delivery learning

Record no-bid, loss, win, debrief, award, amendments, actual cost, delivery performance, penalties, and realized margin. Reviewed results feed evaluation datasets and model calibration.

## 7. Functional requirements

### FR-01 — Source adapters

- Poll official datasets on their published cadence.
- Support incremental, idempotent imports and replay.
- Keep a source-adapter contract so broader public-sector portals can be added without changing domain models.
- Reconcile counts and raise data-quality incidents for unexpected gaps.
- Never use unrestricted HTML crawling as the default path.

### FR-02 — Immutable evidence

- Store raw notices and documents in immutable object storage.
- Compute content hashes and preserve retrieval time, URL, media type, language, and access method.
- Record document versions and supersession relationships.
- Keep source text separate from extracted text and unofficial translations.

### FR-03 — Typed tender dossier

- Validate normalized records with strict Pydantic domain models.
- Retain both reference and solicitation identifiers.
- Separate source status from amendment events.
- Represent missing, conflicting, calculated, estimated, inferred, and translated values explicitly.
- Attach citations to every material extracted field.

#### Required opportunity field catalogue

The dossier must preserve the user's requested trading view without implying that CanadaBuys publishes every field. Each value carries one of Published, Calculated, Estimated, Inferred, Translated, Unknown, Conflicting, or Not applicable, plus its evidence and reviewer state.

| Group | Required fields and handling |
|---|---|
| Identity | Reference number, solicitation number, title, notice type, procurement category, classification codes and canonical URL |
| Scope policy | Goods, services, or services related to goods; exclude clearly classified construction; route mixed or ambiguous scope to human review rather than silently excluding it |
| Notice state | Open, closed, cancelled, awarded, amended or other exact source status; amendment is also retained as a versioned event, not used as a replacement for open/closed status |
| Dates | Publication, amendment, question, site-visit, closing, award, contract start and contract end dates, always with source time zone where available |
| Buyer | Procuring organization, department/agency/Crown entity, branch, contact and buying region where published |
| Supplier intent | Intended, pre-identified or incumbent supplier only when expressly published, including the procurement mechanism and challenge period where applicable; otherwise Not published |
| Contract | One-time/spot requirement, standing offer or supply arrangement, initial term, quantities, options, extension count/duration and maximum potential term |
| Delivery | Delivery/performance location, named place, schedule, shipping responsibility, freight, title/risk transfer and any published Incoterm; preserve the source term and never convert an unfamiliar abbreviation into FOB/CIF without evidence |
| Evaluation and acceptance | Mandatory and rated criteria, point allocation, basis of selection, testing, inspection, samples, demonstrations, acceptance method and named third-party approval body |
| Participation | Registration, prequalification, security, Controlled Goods, Indigenous set-aside/PSIB, Canadian-content or other preference, trade agreements, licences, certifications, insurance, bonding, financial capacity, experience, named roles, manufacturer authorization, regional presence, site visit and subcontracting rules |
| Value | Published estimate, budget, ceiling, minimum/maximum commitment and currency; separately calculated low/base/high order-value estimate with inputs and confidence |
| Offer range | Published offer or bid range only when the source expressly provides it; do not represent award value, winning price, comparable contracts or an estimate as the range of all offers |
| Submission | Method/channel, portal, file and form rules, technical/financial separation, signatures, bid validity, bid security, closing timestamp and time zone |
| Language | Original notice/document language, official bilingual relationship where available, working display language and clear Unofficial AI translation label |
| Links | Notice, amendments, attachments, tendering-system page, buyer-provided supporting pages and every authorized additional-information URL, each with retrieval and version status |

The detail-on-demand view must also show:

- all explicitly published participation and performance requirements;
- operational readiness checks that are normally needed but not published, labelled Internal readiness check or Analyst assumption and never Tender requirement;
- missing, ambiguous, contradictory or inaccessible information that should be clarified with the buyer;
- the evidence, impact, deadline, proposed question and affected decision for every clarification item;
- a hard-gate-first opportunity rank, estimated order range and commercial scenarios;
- recommended markup and gross-margin ranges generated from deterministic cost/risk scenarios, never as an unsupported universal percentage, with final price reserved for an authorized commercial approver.

For awards and contract history, the normalized view must include buyer, product/service description and classification, awarded supplier, contract value and currency, original versus amended cumulative value, award/start/end dates, duration and options, solicitation linkage, contract amendments, and manufacturer or delivery supplier when expressly published. Missing manufacturer/supplier detail remains Not published; entity linkage confidence and human verification status are mandatory.

### FR-04 — Document intelligence

- Extract text from PDF, DOCX, XLSX, HTML, and common image formats.
- Use OCR only when native text is unavailable or inadequate.
- Preserve page, sheet, table, section, and paragraph locators.
- Detect document-language and maintain bilingual relationships.
- Quarantine corrupt, encrypted, unsupported, or suspicious files for review.

### FR-05 — Amendment intelligence

- Compare notice and attachment versions.
- Classify changes by deadline, eligibility, scope, quantity, specification, evaluation, contract, pricing, form, and informational impact.
- Invalidate every dependent artifact using a traceable dependency graph.
- Notify owners and require reapproval for material changes.

### FR-06 — Company profile and supplier evidence

- Version all company facts and attachments.
- Track evidence owners, expiry, verification, permitted entities, and usage restrictions.
- Prevent expired or unverified evidence from silently satisfying a mandatory requirement.
- Support supplier, subcontractor, manufacturer, and partner entities separately.

### FR-07 — Compliance matrix

- Preserve exact requirement wording and citation.
- Distinguish mandatory, rated, acceptance, contractual, and commercial-readiness items.
- Link requirement to evidence, owner, response, score, reviewer, and status.
- Block progression when fatal items are Fail or unresolved Unknown.

### FR-08 — Commercial analysis

- Support goods, services, and services-related-to-goods cost templates.
- Distinguish cost, markup, margin, currency, tax, contingency, ceiling, minimum, and guarantee.
- Store scenario assumptions and sensitivity results.
- Prevent a pricing recommendation without commercial approval.

### FR-09 — Multi-agent execution

- Use one supervisor and up to nine specialist roles.
- Fan out only independent work; serialize state-changing or policy-defining work.
- Enforce per-run limits for agents, model requests, tokens, tool calls, elapsed time, retries, and spend.
- Prevent specialist-to-specialist recursive delegation.
- Aggregate typed results with evidence references and explicit limitations.

### FR-10 — Skills and hooks

- Implement versioned skills as PydanticAI capabilities and governed toolsets.
- Use stable IDs and immutable published versions.
- Support on-demand loading for long-tail workflows.
- Apply always-on authorization, evidence, privacy, budget, and audit hooks outside skill instructions.
- Roll back prompts, skills, models, and workflow definitions independently.

### FR-11 — Human-in-the-loop

- Create durable approval tasks tied to exact artifact hashes and definition versions.
- Support approve, reject, request changes, delegate, and expire.
- Record actor, role, reason, timestamp, source state, and changed fields.
- Revoke approval automatically when a material dependency changes.
- Never treat a client-provided approval flag as authorization.

### FR-12 — Drafting and package management

- Generate drafts from the approved compliance matrix and evidence.
- Keep technical and financial content separated when required.
- Detect missing forms, placeholders, inconsistent figures, unsupported claims, and stale attachments.
- Produce a final internal package manifest with hashes.
- Do not upload or submit externally.

### FR-13 — Award and contract learning

- Link opportunity, bid decision, submitted version, award, contract, amendment, and delivery records.
- Preserve original and cumulative contract amounts.
- Track match confidence and human verification.
- Feed only reviewed outcomes into scoring and evaluation datasets.

### FR-14 — Search, filters, and exports

- Search by identifiers, buyer, title, classification, category, location, dates, supplier, status, eligibility, score, owner, and workflow state.
- Save views and team watchlists.
- Export source-linked tender dossiers, compliance matrices, commercial summaries, and audit packages in approved formats.

## 8. Minimal transparent UI

The UI should use the existing Verel React shell and design primitives. It should contain:

1. Work inbox — new tenders, amendments, approvals, deadlines, failures, and assignments.
2. Opportunity pipeline — configurable stages from New through Outcome.
3. Tender list — compact filters, saved views, freshness, eligibility and priority.
4. Tender workspace — Overview, Evidence, Requirements, Commercial, Response, Activity.
5. Evidence viewer — original document beside extracted field, source locator, version, confidence, and reviewer state.
6. Compliance matrix — requirement-to-evidence grid with hard blockers visible.
7. Pricing workspace — assumptions, scenarios, formulas, approvals, and sensitivity.
8. Agent run timeline — supervisor plan, active agents, tools, durations, token/cost usage, results, failures, retries, and human interventions.
9. Amendment diff — changed sources, impact, invalidated artifacts, and reapproval status.
10. Approval inbox — exact decision, affected artifact hash, risk, approver role, and audit trail.
11. Administration — users/roles, source adapters, company profile, model policy, skills, hooks, budgets, retention, and feature flags.

Every AI-produced value must expose Why, Evidence, Status, Generated by, Model/definition version, and Last reviewed. The default view emphasizes exceptions and human decisions rather than raw agent conversation.

## 9. AI operating boundaries

AI may:

- classify, extract, translate, summarize, compare, rank, calculate, draft, review, and propose;
- call read-only approved tools;
- create internal tasks and approval requests;
- identify contradictions, missing evidence, and clarification candidates.

AI may not:

- invent qualifications, certifications, supplier facts, references, prices, or official requirements;
- turn a commercial assumption into a published requirement;
- approve its own work;
- accept contract terms or deviations;
- expose credentials or confidential supplier information;
- contact a buyer or competitor;
- sign, upload, revise, withdraw, or submit a bid;
- bypass a hard gate, authorization decision, or procurement channel.

## 10. Data model requirements

Minimum authoritative entities:

- Organization, User, Role, Team
- CompanyProfile, CapabilityEvidence, Supplier, Partner, Manufacturer
- Source, SourceSnapshot, Notice, Solicitation, Amendment, Document, DocumentVersion
- TenderField, Citation, Extraction, Translation, Conflict
- Requirement, Criterion, ComplianceAssessment, Clarification
- OpportunityScore, Comparable, Award, Contract, ContractAmendment
- CostModel, CostLine, PricingScenario, Approval
- BidDecision, ResponsePackage, ResponseSection, PackageManifest
- WorkflowRun, AgentRun, AgentTask, ToolCall, UsageRecord, AuditEvent
- Outcome, Debrief, DeliveryActual, ModelEvaluation

All externally sourced and AI-derived entities require tenant, source, version, timestamps, actor or agent identity, and correlation identifiers.

## 11. Non-functional requirements

### Reliability

- Durable recovery across worker restart and transient provider failure.
- Idempotent source ingestion, document processing, notifications, and external-side-effect proposals.
- Material failures finish in a visible terminal state; no silent fallback.
- Initial target: 99.5 percent monthly API availability, RPO no greater than 15 minutes, RTO no greater than 4 hours. Production targets require sponsor approval.

### Performance

- New official-feed record visible within 15 minutes of successful source publication/poll.
- Initial normalized record within 5 minutes for a notice without attachments.
- Standard tender dossier target within 20 minutes after all accessible documents arrive.
- UI read interactions p95 below 500 ms, excluding document download and live AI operations.
- Agent progress visible within 2 seconds of a persisted state change.

### Scale

- Prove 100 active tender workflows without state loss in the pilot. Prove the architecture can support up to 10 concurrent specialist tasks per tender, but enable 3 in Phase 0, promote to 6 for the pilot, and permit 10 only after the documented quality, cost, rate-limit and resilience gates pass.
- Scale worker replicas independently from API/UI.
- Apply provider and tenant concurrency limits with backpressure.

### Security and privacy

- OIDC/SSO, RBAC, tenant isolation, least privilege, encrypted transport and storage.
- Secrets from an approved secret manager, never from prompts or logs.
- Malware scanning and file-type validation before parsing.
- Prompt-injection isolation: source documents are untrusted evidence, never system instructions.
- Redacted structured logs and configurable telemetry content capture.
- Configurable retention and legal hold.
- Canadian data residency, privacy-law applicability, and model-provider retention require formal decisions before production.

### Observability

- OpenTelemetry traces, metrics, and structured logs with correlation_id, tender_id, workflow_id, task_id, agent_id, skill_version, tool_id, tenant_id, model, provider, latency, tokens, cost, status, and error class.
- Do not record secrets, full bid pricing, resumes, security details, or full model content by default.
- Dashboards for source freshness, queue depth, workflow latency, amendment backlog, agent/tool failure, approval wait, token/cost, and quality drift.

### Maintainability

- Strict typed contracts at service and agent boundaries.
- API inputs forbid unknown fields; upstream adapters tolerate and map new fields.
- Version workflows, task messages, domain events, prompts, agents, skills, and model policies.
- Architecture fitness tests prevent direct model access from domain code and prevent side-effecting tools without approval policy.

## 12. Deployment requirements

- One reproducible OCI image per deployable service family.
- Docker Compose overlay for local and integration environments.
- Health, readiness, and dependency checks for every service.
- Non-root containers, read-only filesystem where practical, pinned base images, SBOM, vulnerability scanning, and signed production images.
- Database migrations run as a controlled one-shot job.
- Environment-specific configuration outside images.
- Production deployment target remains an ADR: managed Kubernetes/ECS plus managed PostgreSQL, object storage, and Temporal Cloud or self-hosted Temporal.

## 13. Analytics and product telemetry

Measure:

- notices processed, included, excluded, and blocked;
- analyst active time and cycle time per stage;
- automation rate and human-touch rate;
- extraction citation coverage and human correction rate;
- mandatory-criterion miss rate;
- amendment detection and reassessment latency;
- approval wait time;
- bid/no-bid distribution, win rate, contribution, and realized margin;
- model/tool cost per tender and per submitted bid;
- false-positive shortlist rate and false-negative findings from sampling;
- user adoption and override reasons.

## 14. Success metrics and release gates

| Metric | Baseline | MVP gate | Production pilot target |
|---|---:|---:|---:|
| Qualified opportunities per analyst-week | Measure in Phase 0 | 3x | 10x |
| Active time: discovery to qualified dossier | Measure in Phase 0 | 60 percent reduction | 80 percent reduction |
| Active time: compliance matrix | Measure in Phase 0 | 50 percent reduction | 70 percent reduction |
| Material-field citation coverage | Measure in Phase 0 | at least 95 percent | 100 percent |
| Missed mandatory requirement rate | Measure in Phase 0 | no worse than baseline | zero in audited pilot set |
| Material amendment detection | Measure in Phase 0 | 100 percent in golden set | 100 percent in pilot |
| Unsupported official-fact rate | Measure in Phase 0 | below 1 percent | zero high-severity cases |
| Autonomous external actions | 0 | 0 | 0 |
| Human approval audit coverage | Measure in Phase 0 | 100 percent | 100 percent |
| Agent cost per qualified dossier | Measure in Phase 1 | budget established | within approved unit economics |

No 10x claim may be used externally until a statistically meaningful pilot compares the new workflow with the approved baseline and quality is non-inferior.

## 15. Release phases

### R0 — POC and shadow baseline

Official-feed ingestion, immutable evidence, one tender dossier, four specialist agents, no production decisions.

### R1 — Read-only MVP

Discovery, documents, amendments, company fit, compliance matrix, award intelligence, transparent UI, approvals, and export.

### R2 — Supervised commercial and bid workspace

Costing, pricing scenarios, bid/no-bid, drafting, review, package freeze, and human submission checklist.

### R3 — Controlled production pilot

6–10 agents, hardened operations, calibrated evaluations, role separation, incident response, and measurable throughput.

### R4 — Scale and approved integrations

Additional public-sector sources, ERP/CRM integrations, delivery learning, and only formally authorized external integrations.

## 16. Dependencies

- Verel capability, runtime, event, identity, and UI contracts.
- Official CanadaBuys data sources and source-specific access permissions.
- PydanticAI 2.x, pinned and conformance-tested.
- Temporal proof of concept and operational ownership decision.
- PostgreSQL and object storage.
- Model provider, region, retention, and budget decision.
- Procurement SME availability for golden datasets and acceptance.
- Security/privacy review before sensitive company or personnel evidence enters the system.

## 17. Open sponsor decisions

| ID | Decision | Needed by |
|---|---|---|
| OD-01 | Federal-only MVP or all CanadaBuys sources | Phase 0 start |
| OD-02 | Company entities, categories, regions, and capacity profile | Phase 0 |
| OD-03 | Model provider(s), Canadian region, retention, and confidential-data terms | Architecture gate |
| OD-04 | Temporal Cloud versus self-hosted Temporal | Production design |
| OD-05 | Existing Verel deployment versus separately isolated environment | Architecture gate |
| OD-06 | SSO provider and role owners | MVP build |
| OD-07 | Pricing approval thresholds and separation of duties | Commercial build |
| OD-08 | Record retention, legal hold, and deletion policy | Security gate |
| OD-09 | Whether any portal permits a supported submission integration | R4 only |
| OD-10 | Pilot users, baseline sample, and success-signoff owner | Phase 0 |

## 18. Product acceptance

The product may enter a controlled pilot only when:

- every functional requirement in the pilot scope has an accepted test;
- the source and amendment golden datasets pass;
- all material fields in the pilot have citations;
- no fatal Unknown can reach Bid Approved;
- AI cannot execute external state changes;
- approvals are bound to immutable artifact versions;
- restart, retry, cancellation, stale-approval, and duplicate-delivery tests pass;
- users complete a realistic tender workflow through the UI;
- operational dashboards, alerts, backups, restore, incident, and rollback procedures are proven;
- procurement, commercial, security/privacy, and product owners sign off.
