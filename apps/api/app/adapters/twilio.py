from dataclasses import dataclass


@dataclass
class TwilioInboundEvent:
    call_sid: str
    from_number: str
    to_number: str
    call_status: str


class TwilioAdapter:
    """Twilio-specific logic is isolated here to keep providers swappable."""

    @staticmethod
    def parse_inbound_webhook(form_data: dict) -> TwilioInboundEvent:
        return TwilioInboundEvent(
            call_sid=form_data.get("CallSid", ""),
            from_number=form_data.get("From", ""),
            to_number=form_data.get("To", ""),
            call_status=form_data.get("CallStatus", "ringing"),
        )
