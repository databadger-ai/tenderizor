# CanadaBuys AI Tender Assistant

Developer handoff package for a supervised AI system that helps a trading and bid team discover, qualify, price, draft, review, and learn from Canadian government tender opportunities.

| Field | Value |
|---|---|
| Status | Phase-0 MVP implemented for local development; production promotion gates remain open |
| Date | 2026-08-06 |
| Intended host | Verel consolidated platform |
| Agent runtime | PydanticAI 2.x behind Verel-owned typed contracts |
| Workflow runtime | Temporal, subject to the Phase 0 proof-of-concept gate |
| Deployment | OCI containers and Docker Compose for local development |
| Primary interface | Transparent, exception-first React workspace |
| Automation posture | Read and draft by default; named humans authorize consequential decisions and every external action |

## Start here

For the runnable MVP and its deliberate limits, start with [IMPLEMENTATION.md](IMPLEMENTATION.md).
The original product and architecture documents remain the source of truth for promotion beyond
the isolated Phase-0 slice.

### Run the MVP locally

1. Ensure `.env.local` exists from `.env.example` and set `OPENAI_API_KEY` without committing it.
2. Run `docker compose up -d --build`.
3. Open `http://localhost:3100`; API liveness is at `http://localhost:8000/health/live`.
4. Run `make qa` for static checks, unit/integration tests, and production builds. Run `make smoke`
   after the stack is healthy.

The local workflow is manual source ingestion, evidence-linked AI analysis, a deterministic bid
gate, human review/correction, and an append-only audit timeline. It cannot communicate with a
buyer or submit a bid.

### Design package

1. [Product requirements](01-PRD.md)
2. [Target architecture](02-ARCHITECTURE.md)
3. [Agents, skills, and hooks](03-AGENTS-SKILLS-HOOKS.md)
4. [Phased action plan](04-ACTION-PLAN.md)
5. [Engineering task backlog](05-TASKS.md)
6. [QA and acceptance matrix](06-QA-ACCEPTANCE.md)
7. [Risks and architecture decisions](07-RISKS-DECISIONS.md)
8. [Evidence and references](08-REFERENCES.md)

## Executive decision

Build this as a new tender-intelligence capability in the existing Verel platform, not as a separate product fork and not as one microservice per AI agent.

Use coarse-grained deployable services for API/UI, ingestion, documents, agent workflows, and notifications. Run the supervisor and 6–10 specialist roles through horizontally scalable PydanticAI workers. Temporal owns durable scheduling, retries, fan-out/fan-in, cancellation, timeouts, and human approval waits. PostgreSQL owns business state; object storage owns immutable source documents. The model never owns authorization or the source of truth.

The first production release is read-only and draft-only. It may recommend Bid or No Bid, propose pricing, and prepare a response package, but it cannot contact a buyer, accept terms, sign, upload, revise, withdraw, or submit a bid.

## What “10x faster” means

The project must measure the team’s current baseline before claiming improvement. The north-star target is:

- at least 10 times more qualified opportunities reviewed per analyst-week;
- no increase in missed mandatory requirements or compliance defects;
- 100 percent of material extracted facts linked to an exact source before the production pilot is used to support a 10x claim;
- at least 80 percent reduction in median active analyst time for discovery-to-qualified-dossier work;
- at least 70 percent reduction in compliance-matrix preparation time;
- zero autonomous external submissions or buyer communications.

The 10x claim is a release outcome to prove in a controlled pilot, not an assumption embedded in the business case.

## Non-negotiable design rules

- Official feeds and approved source adapters are the ingestion foundation; HTML crawling is not.
- Current solicitation documents and amendments are authoritative; AI summaries are not.
- Published requirements and analyst assumptions are separate registers.
- Every material fact has source, version, locator, extraction status, and reviewer state.
- Missing information remains Not published or Unknown; the system never fills gaps as fact.
- Hard eligibility failures override commercial scores.
- PydanticAI is replaceable. Domain rules, permissions, state, approvals, and side effects remain application-owned.
- Specialist agents cannot recursively spawn more agents. Only the supervisor may fan out. The Phase 0 ceiling is 3, the pilot ceiling is 6 after its promotion gate, and 10 is an upper capability limit enabled only after the quality, cost and resilience gates pass.
- Deterministic code handles downloads, parsing, calculations, status transitions, deadlines, and policy rules. LLMs handle language-heavy interpretation and drafting.
- Any material amendment invalidates affected analysis, pricing, approvals, and response sections.
- All externally consequential steps require authenticated, role-authorized human approval.

## Delivery assumptions requiring sponsor confirmation

- MVP scope is federal CanadaBuys, open non-construction opportunities.
- Mixed construction/non-construction records are routed to manual review.
- The solution is added to Verel as a capability manifest and deployable worker set.
- English is the working UI language; original French text is preserved and AI translations are labelled unofficial.
- A Canada-region deployment and a model-provider data-retention posture are preferred but remain procurement/security decisions.
- Direct automated submission is out of scope unless CanadaBuys or a downstream portal provides and authorizes a suitable integration.

## Recommended implementation team

- 1 technical lead or principal engineer
- 2 backend and workflow engineers
- 1 AI/PydanticAI engineer
- 1 frontend engineer
- 1 platform/SRE engineer
- 1 QA/evaluation engineer
- 0.5 procurement subject-matter expert
- 0.25 security/privacy reviewer

Indicative delivery is 14–18 calendar weeks and roughly 75–105 person-weeks, subject to the Phase 0 baseline, source-access, identity, model-provider, and deployment decisions.

## Package acceptance

This package is ready for engineering estimation when the sponsor approves the scope and open decisions in the PRD. It does not authorize production data access, buyer communication, or bid submission.
