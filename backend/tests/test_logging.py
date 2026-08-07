import json

import pytest

from app.core.config import Settings
from app.core.logging import configure_logging, get_logger


def test_logger_acquired_before_configuration_emits_required_json(
    capsys: pytest.CaptureFixture[str],
) -> None:
    logger = get_logger("test-component")
    configure_logging(Settings(environment="test"))

    logger.info(
        "test_event",
        correlation_id="11111111-1111-4111-8111-111111111111",
        request_id="22222222-2222-4222-8222-222222222222",
        status="SUCCEEDED",
    )

    captured = capsys.readouterr()
    event = json.loads(captured.out)
    assert event["event"] == "test_event"
    assert event["severity"] == "INFO"
    assert event["component"] == "test-component"
    assert event["correlation_id"] == "11111111-1111-4111-8111-111111111111"
    assert event["request_id"] == "22222222-2222-4222-8222-222222222222"
    assert event["status"] == "SUCCEEDED"
    assert event["timestamp"]
    assert "error_class" in event
