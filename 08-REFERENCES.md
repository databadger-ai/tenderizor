# Evidence and References

Accessed 2026-07-31 unless otherwise noted. Primary and authoritative sources are used for material design claims.

## 1. Repository evidence

- [Verel fleet agent guide](../../CLAUDE.md)
- [Verel Team Contract](../ARCHITECTURE.md)
- [Verel platform architecture](../../platform/docs/architecture.md)
- [Existing PydanticAI refactor proposal](../../platform/docs/PYDANTIC_AI_REFACTOR_PROPOSAL.md)
- [Platform Python dependencies](../../platform/pyproject.toml)
- [Frontend dependencies and commands](../../platform/frontend/package.json)
- [Platform Docker Compose](../../platform/compose.yaml)

Relevant established constraints:

- one consolidated platform and one frontend shell;
- products/features are capability manifests, not separate codebases;
- stable runtime/event contracts;
- explicit user context and server-side tool filtering;
- mutations propose and require human approval;
- OpenTelemetry/Langfuse-compatible observability;
- Docker-based deployment and shared image patterns.

The existing PydanticAI proposal was an untracked workspace file when this package was created. It was treated as read-only user work and was not modified.

## 2. CanadaBuys sources and data

- [Procurement and contracting data](https://canadabuys.canada.ca/en/procurement-and-contracting-data)
- [CanadaBuys open-data supporting documentation](https://donnees-data.tpsgc-pwgsc.gc.ca/ba2/ac-cb/soutien-support-eng.html)
- [CanadaBuys data dictionary](https://donnees-data.tpsgc-pwgsc.gc.ca/ba2/ac-cb/achatscanada-canadabuys-dd.xml)
- [Open tender notices CSV](https://canadabuys.canada.ca/opendata/pub/openTenderNotice-ouvertAvisAppelOffres.csv)
- [New tender notices CSV](https://canadabuys.canada.ca/opendata/pub/newTenderNotice-nouvelAvisAppelOffres.csv)
- [Complete tender notices CSV](https://canadabuys.canada.ca/opendata/pub/tenderNoticeComplete-avisAppelOffresComplet.csv)
- [Complete award notices CSV](https://canadabuys.canada.ca/opendata/pub/awardNoticeComplete-avisAttributionComplet.csv)
- [Complete contract history CSV](https://canadabuys.canada.ca/opendata/pub/contractHistoryComplete-contratsOctroyesComplet.csv)
- [Searching tender opportunities](https://canadabuys.canada.ca/en/support/searching-tender-opportunities)
- [Following a saved search or tender notice](https://canadabuys.canada.ca/en/support/following-saved-search-or-tender-notice)
- [Viewing tender opportunities](https://canadabuys.canada.ca/en/support/viewing-tender-opportunities)
- [Searching award notices and contract history](https://canadabuys.canada.ca/en/support/searching-award-notices-and-contract-history)
- [CanadaBuys robots instructions](https://canadabuys.canada.ca/robots.txt)

Architecture implications:

- use official datasets/subscriptions rather than a 200-row HTML view;
- preserve solicitation and reference identifiers;
- treat amendment separately from status;
- model missing/access-blocked data explicitly;
- support multiple access paths and downstream portals;
- maintain separate adapters for federal and non-federal scope.

## 3. Procurement and submission controls

- [Checklist for preparing a bid](https://canadabuys.canada.ca/en/support/checklist-preparing-bid)
- [How bids are evaluated and selected](https://canadabuys.canada.ca/en/getting-started/preparing-sell-government/how-bids-evaluated-and-selected)
- [Registering on SAP Business Network](https://canadabuys.canada.ca/en/support/registering-sap-ariba-guide-businesses)
- [Responding through SAP Business Network Discovery](https://canadabuys.canada.ca/en/support/responding-tender-opportunities-ariba-discovery)
- [Submitting through CanadaBuys Connect](https://canadabuys.canada.ca/en/support/submitting-bid-receiving-unit-using-connect)
- [Advanced Contract Award Notice](https://canadabuys.canada.ca/en/buyer-s-portal/buyer-s-guide/create-solicitation/tender-notices/advanced-contract-award-notice)
- [Standing offers and supply arrangements](https://canadabuys.canada.ca/en/tender-opportunities/standing-offers-and-supply-arrangements)
- [Security screening for government contracts](https://www.canada.ca/en/public-services-procurement/services/industrial-security/security-requirements-contracting/security-screening-government-contracts.html)
- [Supplier integrity and compliance](https://www.canada.ca/en/public-services-procurement/services/standards-oversight/supplier-integrity-compliance/about.html)
- [Indigenous procurement considerations](https://canadabuys.canada.ca/en/buyer-s-portal/buyer-s-guide/plan/socioeconomic-considerations/indigenous-considerations)
- [Buy Canadian Policy](https://canadabuys.canada.ca/en/buy-canadian-policy)
- [Competition Bureau guidance on bid-rigging](https://competition-bureau.canada.ca/en/bid-rigging-price-fixing-and-other-agreements-between-competitors)
- [Guide on the Use of Agentic Artificial Intelligence](https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/responsible-use-ai/guide-use-agentic-artificial-antelligence.html)
- [PIPEDA requirements in brief](https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/pipeda_brief?wbdisable=true)

Architecture implications:

- the solicitation and amendments control;
- mandatory criteria are pass/fail;
- submission mechanics are channel-specific;
- registration, security, integrity, set-asides and policy conditions are tender-specific;
- AI approval cannot replace authorized human accountability;
- privacy and confidential bid information require explicit handling decisions.

## 4. PydanticAI

- [Agents, typed dependencies, outputs, streaming, usage and concurrency](https://pydantic.dev/docs/ai/core-concepts/agent/)
- [Dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/)
- [Structured output](https://pydantic.dev/docs/ai/core-concepts/output/)
- [Capabilities](https://pydantic.dev/docs/ai/capabilities/overview/)
- [On-demand capabilities](https://pydantic.dev/docs/ai/capabilities/on-demand/)
- [Lifecycle hooks](https://pydantic.dev/docs/ai/core-concepts/hooks/)
- [Toolsets and filtering/composition](https://pydantic.dev/docs/ai/tools-toolsets/toolsets/)
- [Deferred tools and human approval](https://pydantic.dev/docs/ai/tools-toolsets/deferred-tools/)
- [Multi-agent patterns](https://pydantic.dev/docs/ai/guides/multi-agent-applications/)
- [MCP overview](https://pydantic.dev/docs/ai/mcp/overview/)
- [Durable execution overview](https://pydantic.dev/docs/ai/capabilities/durable_execution/overview/)
- [Temporal integration](https://pydantic.dev/docs/ai/capabilities/durable_execution/temporal/)
- [DBOS integration](https://pydantic.dev/docs/ai/capabilities/durable_execution/dbos/)
- [PydanticAI observability and OpenTelemetry](https://pydantic.dev/docs/ai/integrations/logfire/)
- [Pydantic Evals](https://pydantic.dev/docs/ai/evals/evals/)
- [Testing](https://pydantic.dev/docs/ai/guides/testing/)
- [Version policy](https://pydantic.dev/docs/ai/project/version-policy/)

Key evidence:

- agents support typed dependencies and validated structured outputs;
- capabilities bundle tools, hooks, instructions, model settings and model selection;
- on-demand capabilities keep long-tail tool definitions out of context until loaded;
- toolsets can be combined, filtered and prefixed;
- multi-agent delegation supports shared usage accounting and run limits;
- deferred-tool approval is explicitly not a security authorization boundary;
- full tool/event execution should use full event streaming/iteration rather than final-output-only streaming semantics;
- OpenTelemetry backends can be used without making Logfire mandatory;
- durable execution is officially supported through Temporal, DBOS, Prefect and Restate;
- stable IDs, serialization, idempotency and workflow execution context matter for durable replay.

## 5. Temporal

- [Temporal documentation](https://docs.temporal.io/)
- [Python SDK developer guide](https://docs.temporal.io/develop/python)
- [Python workflow message passing](https://docs.temporal.io/develop/python/workflows/message-passing)
- [Temporal workflow execution](https://docs.temporal.io/workflow-execution)
- [Temporal samples server repository](https://github.com/temporalio/samples-server)

Key evidence:

- workflows resume through failures and long waits;
- Queries read state, Signals asynchronously change state, and Updates can validate/change state and return a result;
- workflow wait conditions support approval-style pauses;
- workers and task queues separate workflow/activity execution;
- workflow determinism, activity idempotency, versioning and payload compatibility are production concerns.

## 6. Platform and delivery

- [Docker Compose documentation](https://docs.docker.com/compose/)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
- [ICC Incoterms 2020](https://iccwbo.org/business-solutions/incoterms-rules/incoterms-2020/)

## 7. Evidence limitations

- No production CanadaBuys submission API was established by this review.
- Broader-public-sector portals have source-specific accounts, fees, terms and technical behavior; they require adapter-by-adapter investigation.
- Company capability, supplier, pricing, legal, privacy, residency, retention and model-provider choices were not supplied.
- The 10x outcome has not been measured; it is a controlled-pilot target.
- Temporal is a conditional recommendation pending the actual team’s POC and operating decision.
- PydanticAI minor releases may add events or optional fields; the project must pin and conformance-test a selected version.
