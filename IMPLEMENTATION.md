# MVP implementation boundary

This workspace implements the document-defined Phase-0 read-only vertical slice:

`source record -> dossier -> cited requirements -> analyst correction -> audit event`

It is an isolated development capability because the intended Verel application shell is not present in this workspace. Public API contracts, workflow boundaries, and UI feature boundaries are kept explicit so the capability can be integrated into Verel later.

## Included

- Manual ingestion of a tender record and source text.
- Immutable source-text hash and line-addressable evidence.
- Typed OpenAI/PydanticAI analysis through the Responses API.
- Durable Temporal workflow entry; model I/O runs in Temporal activities.
- Material fields, eligibility recommendation, evidence citations, missing facts, and risks.
- Mandatory, rated, and internal-readiness requirements kept distinct.
- Deterministic hard gate: every mandatory `FAIL` or `UNKNOWN`, plus any explicitly fatal
  non-mandatory `FAIL` or `UNKNOWN`, blocks bidding regardless of the model recommendation.
- Human correction/review with an append-only audit event.
- Transparent React workbench for opportunities, evidence, requirements, and activity.
- Structured, redacted logs with request and correlation identifiers.

## Explicitly disabled

- Buyer communications, bid upload, submission, revision, withdrawal, or signing.
- Portal credentials and unrestricted HTML scraping.
- Autonomous price approval or compliance certification.
- Production SSO, tenant administration, Canada-region deployment, and provider-retention claims.
- Claims that this prototype has achieved the PRD's 10x production target.

## Promotion gates

Production use still requires the source corpus, procurement review, Verel integration, OIDC/RBAC ownership, official CanadaBuys adapter, object storage, malware scanning, backup/restore evidence, security/privacy review, and the full release gates in `06-QA-ACCEPTANCE.md`.
