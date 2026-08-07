import asyncio
from hashlib import sha256

from httpx import AsyncClient


async def create_tender(client: AsyncClient, source_text: str) -> dict[str, object]:
    response = await client.post(
        "/api/v1/tenders",
        json={
            "title": "Network Equipment RFQ",
            "buyer": "Example Department",
            "deadline": "2026-09-01T15:00:00-04:00",
            "source_text": source_text,
            "reference_number": "REF-100",
            "solicitation_number": "SOL-200",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


async def test_tender_create_list_get_and_source_hash(client: AsyncClient) -> None:
    source = " Official notice \nClosing date: September 1\n"
    created = await create_tender(client, source)
    assert created["source_sha256"] == sha256(source.encode()).hexdigest()
    assert created["line_count"] == 2
    assert created["buyer"] == "Example Department"

    listed = await client.get("/api/v1/tenders")
    assert listed.status_code == 200
    assert listed.json()["total"] == 1
    assert "source_text" not in listed.json()["items"][0]

    fetched = await client.get(f"/api/v1/tenders/{created['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["source_text"] == source


async def test_whitespace_only_source_is_rejected(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/tenders",
        json={"title": "Tender", "source_text": " \n\t "},
    )
    assert response.status_code == 422


async def test_analysis_is_queued_then_persists_typed_blocked_result(client: AsyncClient) -> None:
    tender = await create_tender(
        client,
        "Official tender\nMANDATORY FAIL: Supplier must hold certification X",
    )
    started = await client.post(
        f"/api/v1/tenders/{tender['id']}/analysis-runs",
        json={"requested_by": "analyst-1"},
    )
    assert started.status_code == 202
    assert started.json()["status"] == "QUEUED"
    run_id = started.json()["run_id"]

    for _ in range(20):
        run = await client.get(f"/api/v1/analysis-runs/{run_id}")
        assert run.status_code == 200
        if run.json()["status"] == "SUCCEEDED":
            break
        await asyncio.sleep(0.01)
    body = run.json()
    assert body["status"] == "SUCCEEDED"
    assert body["analysis"]["gate_outcome"] == "BID_BLOCKED"
    assert body["analysis"]["requirements"][0]["status"] == "FAIL"
    citation = body["analysis"]["requirements"][0]["citations"][0]
    assert citation == {
        "line_start": 2,
        "line_end": 2,
        "quote": "MANDATORY FAIL: Supplier must hold certification X",
    }

    listed = (await client.get("/api/v1/tenders")).json()["items"][0]
    assert listed["latest_run_id"] == run_id
    assert listed["latest_run_status"] == "SUCCEEDED"
    assert listed["recommendation"] == "REVIEW"
    assert listed["gate_outcome"] == "BID_BLOCKED"

    detail = (await client.get(f"/api/v1/tenders/{tender['id']}")).json()
    assert detail["latest_run_id"] == run_id


async def test_correction_appends_activity_event(client: AsyncClient) -> None:
    tender = await create_tender(client, "Official tender")
    corrected = await client.post(
        f"/api/v1/tenders/{tender['id']}/corrections",
        json={
            "actor_id": "reviewer-7",
            "action": "CORRECTION",
            "reason": "Corrected buyer name from source",
            "field_path": "buyer",
            "previous_value": "Wrong Department",
            "corrected_value": "Example Department",
        },
    )
    assert corrected.status_code == 201
    assert corrected.json()["action"] == "CORRECTION"

    activity = await client.get(f"/api/v1/tenders/{tender['id']}/activity")
    assert activity.status_code == 200
    assert activity.json()["total"] == 2
    assert [item["action"] for item in activity.json()["items"]] == [
        "CORRECTION",
        "TENDER_CREATED",
    ]


async def test_validation_error_does_not_echo_source_text(client: AsyncClient) -> None:
    sensitive_source = "SENSITIVE SOURCE BODY"
    response = await client.post(
        "/api/v1/tenders",
        json={"title": "Tender", "source_text": sensitive_source, "unexpected": True},
    )
    assert response.status_code == 422
    assert sensitive_source not in response.text
    assert response.json()["error"]["code"] == "validation_error"


async def test_readiness_reports_database_and_temporal_separately(client: AsyncClient) -> None:
    response = await client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "database": {"status": "ready", "error_class": None},
        "temporal": {"status": "ready", "error_class": None},
    }
