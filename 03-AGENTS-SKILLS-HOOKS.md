# Agents, Skills, and Hooks

## 1. Operating model

The AI team has one supervisor and nine possible specialist roles. A tender does not automatically invoke all ten. The workflow activates the smallest sufficient team, normally 6–8 roles, with ten as a hard ceiling.

Only the supervisor may delegate. Specialists receive typed tasks, bounded evidence references, explicit tool allowlists, budgets, and expected output schemas. They cannot delegate or modify workflow state.

Temporal owns execution order, durable retries, deadlines, human waits and joins. PydanticAI owns each bounded reasoning run.

## 2. Agent roster

| ID | Role | Primary responsibility | Required output | Prohibited authority |
|---|---|---|---|---|
| AG-00 | Tender Supervisor | Plan lanes, dispatch, reconcile, preserve conflicts, synthesize next action | TenderSynthesis and proposed workflow action | Cannot approve, price, contact, sign or submit |
| AG-01 | Discovery Analyst | Classify notice, category, buyer, dates, relevance and access path | DiscoveryFinding | Cannot scrape prohibited paths or treat inaccessible data as absent |
| AG-02 | Evidence and Amendment Analyst | Extract cited fields, inventory documents, compare versions, assess amendment impact | EvidenceDossier and AmendmentImpact | Cannot resolve conflicts by guessing |
| AG-03 | Eligibility and Compliance Analyst | Build mandatory/rated matrix and hard-gate assessment | ComplianceFinding | Cannot convert assumptions into official requirements or override fatal gates |
| AG-04 | Company and Supplier Fit Analyst | Match company, partner, personnel, licence, capacity and evidence | SupplierFitFinding | Cannot assert unverified qualifications or commit suppliers |
| AG-05 | Market and Award Analyst | Find lawful comparables, awards, contract history and buyer patterns | MarketFinding | Cannot infer losing bids or use confidential competitor data |
| AG-06 | Commercial and Pricing Analyst | Build fully burdened cost, scenarios, margin and risk-adjusted economics | CommercialFinding | Cannot set or approve final price |
| AG-07 | Contract and Clarification Analyst | Identify contract risk, missing information and draft clarification questions | ContractRiskFinding and ClarificationDraft | Cannot provide final legal opinion or contact buyer |
| AG-08 | Bid Strategy and Drafting Analyst | Build response plan and draft source-backed sections | ResponsePlan and DraftSections | Cannot invent evidence, sign or finalize |
| AG-09 | Independent Red-Team Reviewer | Challenge compliance, evidence, arithmetic, consistency, amendments and unsupported claims | ReviewFinding with severity/disposition | Cannot review artifacts it authored or waive defects |

## 3. Agent activation matrix

| Workflow stage | Always | Conditional |
|---|---|---|
| Discovery | AG-00, AG-01 | AG-02 for attachments |
| Initial dossier | AG-00, AG-02, AG-03, AG-04 | AG-05 for material opportunities |
| Bid/no-bid | AG-00, AG-03, AG-04, AG-05, AG-06, AG-07 | AG-09 for high-risk decisions |
| Drafting | AG-00, AG-02, AG-03, AG-06, AG-07, AG-08, AG-09 | additional technical contributor agent only by approved extension |
| Amendment | AG-00, AG-02 | every agent whose artifact dependency is affected |
| Post-award | AG-00, AG-05, AG-06, AG-09 | delivery specialist in a future phase |

## 4. Agent task contract

Every run receives:

- tenant, actor, roles and correlation context;
- tender, workflow, task and source snapshot identifiers;
- objective and expected output schema;
- small artifact references rather than entire conversations;
- explicit evidence scope;
- allowed skills/capabilities and tool allowlist;
- denied tools and external-action prohibition;
- deadline, priority and idempotency key;
- model policy and immutable definition versions;
- maximum requests, tokens, tool calls, elapsed time, cost and retries.

Every result returns:

- typed status and recommendation;
- evidence references with document hash and locator;
- published/calculated/estimated/inferred/translated/unknown classification;
- confidence band with rationale;
- assumptions, missing facts, contradictions and limitations;
- requested human decision;
- model, prompt, skill and tool versions;
- usage, latency, cost and safe errors.

## 5. Skills as PydanticAI capabilities

Skills are trusted, versioned domain workflows compiled into PydanticAI capabilities. Stable IDs are durable compatibility contracts. Published versions are immutable.

| Skill ID | Purpose | Loading | Primary agents |
|---|---|---|---|
| skill.canadabuys.source-policy.v1 | Official source hierarchy, categories, statuses and access rules | Always on for source work | AG-01, AG-02 |
| skill.tender.normalize.v1 | Normalize notice identifiers, buyer, dates, language and instrument | On demand | AG-01, AG-02 |
| skill.document.evidence-extraction.v1 | Extract fields with locators and evidence status | On demand | AG-02 |
| skill.amendment.impact.v1 | Compare versions and map invalidation | On demand | AG-02, AG-00 |
| skill.compliance.matrix.v1 | Mandatory/rated criteria and evidence mapping | On demand | AG-03 |
| skill.eligibility.canada.v1 | Registration, security, integrity and solicitation-specific gates | On demand | AG-03 |
| skill.supplier-fit.v1 | Company/supplier capability and evidence matching | On demand | AG-04 |
| skill.market-comparables.v1 | Award and contract-history matching | On demand | AG-05 |
| skill.commercial.goods.v1 | Landed-cost and goods pricing model | On demand | AG-06 |
| skill.commercial.services.v1 | Labour, overhead, utilization and service pricing model | On demand | AG-06 |
| skill.contract-risk.v1 | Contract terms, options, acceptance and clarification risks | On demand | AG-07 |
| skill.bid.strategy.v1 | Bid/no-bid narrative and win themes from approved evidence | On demand | AG-00, AG-08 |
| skill.response.drafting.v1 | Compliance-matrix-driven drafting | On demand | AG-08 |
| skill.review.red-team.v1 | Independent evidence, compliance and consistency challenge | On demand | AG-09 |
| skill.language.bilingual.v1 | Preserve original language and label unofficial translation | On demand | AG-01, AG-02, AG-08 |
| skill.submission.readiness.v1 | Deterministic final package checklist | On demand; read-only | AG-09 |

Skill instructions may guide reasoning but cannot grant permissions, alter hard gates, change prices, or authorize tools.

## 6. Toolsets

### 6.1 Read-only toolsets

- CanadaBuys dataset and saved-search adapter
- Notice/document retrieval with source-policy enforcement
- Document text, OCR and locator service
- Tender and award search
- Company capability/evidence lookup
- Supplier and manufacturer catalogue lookup
- Currency, tax-rate and approved reference-data lookup
- Pricing calculator and scenario engine
- Citation verifier
- Compliance matrix store
- Artifact renderer/exporter in preview mode

### 6.2 Proposed internal-write toolsets

These change only internal draft state and require workflow/context authorization:

- create or update finding;
- create clarification draft;
- assign owner;
- create approval request;
- create draft response section;
- freeze internal package;
- record human-entered submission receipt.

### 6.3 External-action toolsets

Not present in MVP:

- buyer messaging;
- supplier outreach;
- portal upload;
- bid revision/withdrawal;
- final submission.

A future external-action tool requires an authorized integration, an ADR, threat model, contract tests, explicit role approval, argument-bound receipt, idempotency, and a rollback/containment plan.

## 7. Hooks

Use PydanticAI lifecycle hooks and Verel wrapper hooks for observability and guardrails. Hooks are stateless interceptors; Temporal remains the state machine.

| Hook ID | Point | Responsibility | Failure behavior |
|---|---|---|---|
| hook.context.pin | Before run | Resolve tenant/user, pin source and definition versions, set correlation and budgets | Fail closed |
| hook.prompt.boundary | Before model request | Separate trusted instructions from untrusted documents; minimize context | Fail closed |
| hook.model.policy | Before model request | Enforce approved model/provider/region and fallback policy | Fail closed; no silent fallback |
| hook.budget | Before model/tool request | Enforce request, token, cost, time, tool and concurrency budgets | Pause with BudgetExceeded |
| hook.tool.authorize | Before tool call | Enforce role, tenant, workflow state, allowlist and approval receipt | Deny and security-log |
| hook.tool.idempotency | Before tool call | Bind idempotency key to tool, arguments and artifact/source versions | Return prior result or reject conflict |
| hook.provenance | After tool/result | Attach source, hash, locator, adapter and retrieval metadata | Mark result unusable if missing |
| hook.output.validate | After model result | Validate schema, citation coverage, status labels and confidence | Retry bounded; then fail visible |
| hook.privacy.redact | Before telemetry/persistence | Remove secrets and sensitive payloads from logs/traces | Drop unsafe telemetry field |
| hook.events.translate | Event stream | Translate internal events into stable WorkflowEvent records | Persist ERROR then terminal state |
| hook.amendment.invalidate | Source change | Identify stale artifacts and revoke approvals | Block downstream progression |
| hook.review.independence | Task dispatch | Prevent author from becoming independent reviewer | Reject dispatch |
| hook.audit | All transitions | Append safe actor/agent/action/version/outcome event | Fail closed for consequential actions |

Always-on authorization, prompt-boundary, privacy and audit hooks must not be deferred with a domain skill.

## 8. Supervisor algorithm

~~~mermaid
flowchart TD
    A["Receive typed workflow task"] --> B["Validate prerequisites and budgets"]
    B --> C["Create deterministic lane plan"]
    C --> D["Human-visible plan event"]
    D --> E["Temporal fan-out to eligible specialists"]
    E --> F["Collect typed findings"]
    F --> G{"Required lane failed?"}
    G -- Yes --> H["Retry or create blocking task"]
    G -- No --> I["Validate citations and contracts"]
    I --> J{"Material conflict?"}
    J -- Yes --> K["Preserve dissent and request review"]
    J -- No --> L["Synthesize recommendation"]
    K --> L
    L --> M["Propose next workflow action"]
    M --> N["Temporal enforces gate / human wait"]
~~~

The supervisor proposes; it does not mutate the workflow directly.

## 9. Concurrency, budgets, and backpressure

Default policy:

- Phase 0: no more than 3 concurrent specialist runs per tender;
- pilot: promote to a ceiling of 6 only after the defined quality, cost and resilience gate;
- later: 10 is the hard capability ceiling, enabled only after the second promotion gate;
- 6–10 logical lanes may be queued asynchronously while worker and provider backpressure controls determine actual simultaneous execution;
- 1 active supervisor synthesis;
- no specialist delegation;
- 2 attempts for validation-correctable output;
- retry ownership primarily in Temporal, not multiplied across layers;
- provider token bucket shared across workers;
- per-tenant queue and spend quotas;
- lower-cost model for classification/extraction where evaluation permits;
- stronger model for compliance, strategy and red-team work;
- cancel obsolete tasks immediately after a material amendment.

Required budget fields:

- maximum agent tasks;
- maximum model requests;
- maximum input/output/total tokens;
- maximum tool calls;
- maximum wall-clock duration;
- maximum provider cost;
- maximum document/context bytes;
- maximum parallel tasks;
- deadline reserve.

Budget exhaustion yields a visible partial result and human decision, never an unbounded retry loop.

## 10. Human gates

| Gate | Decision owner | Required evidence |
|---|---|---|
| HG-01 Scope/readiness | Product owner and procurement SME | Source scope, company profile, baseline |
| HG-02 Relevance | Trading analyst or bid manager | Discovery dossier and exclusions |
| HG-03 Eligibility/compliance | Compliance lead | Requirement matrix, evidence, unknowns |
| HG-04 Clarification wording | Bid manager/compliance | Source passage, impact, approved wording |
| HG-05 Bid/no-bid | Bid manager/executive by threshold | Hard gate, score, capacity, expected value |
| HG-06 Pricing | Commercial lead/executive by threshold | Cost model, scenarios, assumptions, risk |
| HG-07 Draft readiness | Bid manager and compliance | Completed matrix, reviews, amendments |
| HG-08 Submission package | Named authorized signatory | Frozen package, hashes, checklist, approvals |
| HG-09 Receipt/outcome correction | Bid manager/auditor | External receipt or authoritative outcome source |

Material source or artifact changes revoke downstream approval automatically.

## 11. Prompt and definition lifecycle

1. Draft in Git or governed admin workspace.
2. Validate schema and policy.
3. Run deterministic unit/contract tests.
4. Run golden tender evaluations.
5. Independent reviewer assesses changes and regressions.
6. Named owner approves immutable version.
7. Deploy to shadow or canary cohort.
8. Monitor quality, cost, latency and overrides.
9. Promote or roll back by version pointer.

No prompt, skill or agent can be edited in place after publication. In-flight workflows remain pinned to compatible versions until completed or explicitly migrated.

## 12. Evaluation framework

### Deterministic checks

- schema validity;
- citation exists and locator resolves;
- arithmetic and pricing reconciliation;
- prohibited action/tool absence;
- state-transition legality;
- amendment invalidation;
- role/separation-of-duties;
- stable event ordering and terminal semantics.

### Golden datasets

Maintain representative cases for:

- goods, services and services related to goods;
- English, French and bilingual material;
- missing fields;
- ACAN and standing-offer/supply-arrangement notices;
- security and special-eligibility requirements;
- complex pricing schedules;
- multiple amendments;
- inaccessible or corrupt documents;
- award/contract linkage ambiguity;
- deliberate prompt injection in source documents;
- no-bid and unknown outcomes.

### Quality metrics

- field precision/recall;
- citation entailment and locator validity;
- mandatory requirement recall;
- published-versus-inferred classification;
- unsupported claim severity;
- human correction and override rate;
- red-team defect escape rate;
- cost, tokens and latency;
- inter-agent disagreement rate;
- calibration of confidence and probability of win.

LLM-as-judge may supplement but never replace deterministic checks and procurement-SME review.

## 13. Failure and retry rules

- Validation failure: retry once or twice with structured error feedback.
- Provider transport failure: Temporal retries with bounded exponential backoff and jitter.
- Provider policy/content failure: no automatic model downgrade unless pre-approved and contract-tested.
- Tool timeout: retry only if idempotent; otherwise require reconciliation.
- Evidence missing: return Unknown; do not ask the model to infer.
- Specialist failure: preserve completed lanes; required lane blocks the join.
- Supervisor failure: retry synthesis from persisted findings, not rerun specialists by default.
- Amendment: cancel obsolete tasks and create new task IDs linked to superseded work.
- Terminal error: persist ERROR and COMPLETE-compatible terminal event so UI/replay cannot hang.

## 14. Agent acceptance criteria

- All agent inputs and outputs validate against versioned schemas.
- 100 percent of material findings are cited or explicitly Unknown.
- No specialist can access a delegation tool.
- No agent can see a mutating external tool in MVP.
- Every run shows budgets, model/tool versions and cost.
- Agent failure and disagreement are visible in the UI.
- Independent review is authored by a distinct run/role.
- Prompt injection tests cannot modify tool policy or workflow state.
- A ten-way fan-out survives partial failure, cancellation and restart.
- A material amendment invalidates the correct findings and approvals without corrupting unrelated work.
