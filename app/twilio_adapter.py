from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from uuid import uuid4


@dataclass
class OutboundDialResult:
    call_sid: str
    status: str


class TwilioVoiceAdapter(Protocol):
    def create_outbound_call(self, *, from_number: str, to_number: str, callback_url: str) -> OutboundDialResult:
        ...


class MockTwilioVoiceAdapter:
    """Temporary adapter used for local dev until real Twilio integration is wired."""

    def create_outbound_call(self, *, from_number: str, to_number: str, callback_url: str) -> OutboundDialResult:
        mock_sid = f"CA{uuid4().hex[:32]}"
        return OutboundDialResult(call_sid=mock_sid, status="queued")
