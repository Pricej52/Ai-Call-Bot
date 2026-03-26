from fastapi.testclient import TestClient

from app.database import initialize_database
from app.main import app


client = TestClient(app)


def setup_module() -> None:
    initialize_database()


def test_inbound_webhook_creates_call_session() -> None:
    response = client.post(
        "/webhooks/twilio/voice/inbound",
        json={
            "CallSid": "CA_test_inbound_1",
            "From": "+15550001111",
            "To": "+15551230000",
            "CallStatus": "ringing",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["call_sid"] == "CA_test_inbound_1"
    assert data["direction"] == "inbound"
    assert data["agent_id"] is not None


def test_outbound_job_creates_job_and_session() -> None:
    response = client.post(
        "/calls/outbound-jobs",
        json={
            "to_number": "+15556667777",
            "from_number": "+15551230000",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "queued"
    assert data["provider_call_sid"].startswith("CA")
    assert data["call_session_id"] > 0
