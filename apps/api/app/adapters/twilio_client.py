from typing import Any

import httpx

from app.core.config import settings


class TwilioClientError(Exception):
    pass


class TwilioClient:
    def __init__(self, account_sid: str, auth_token: str):
        self.account_sid = account_sid
        self.auth_token = auth_token

    async def validate_credentials(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                f"{settings.twilio_base_url}/2010-04-01/Accounts/{self.account_sid}.json",
                auth=(self.account_sid, self.auth_token),
            )
        if response.status_code >= 400:
            raise TwilioClientError("Twilio credential validation failed")
        return response.json()

    async def list_incoming_numbers(self) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(
                f"{settings.twilio_base_url}/2010-04-01/Accounts/{self.account_sid}/IncomingPhoneNumbers.json",
                auth=(self.account_sid, self.auth_token),
            )
        if response.status_code >= 400:
            raise TwilioClientError("Unable to fetch Twilio phone numbers")

        payload = response.json()
        return [
            {
                "sid": phone.get("sid"),
                "phone_number": phone.get("phone_number"),
                "friendly_name": phone.get("friendly_name"),
                "capabilities": phone.get("capabilities", {}),
            }
            for phone in payload.get("incoming_phone_numbers", [])
            if phone.get("phone_number")
        ]
