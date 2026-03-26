import httpx

from app.core.config import settings


class LLMOrchestratorAdapter:
    """Interface boundary for text generation for telephony voice turns."""

    async def respond(self, system_prompt: str, user_message: str) -> str:
        if not settings.openai_api_key:
            return "Thanks for calling. Could you please repeat that with a bit more detail?"

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.4,
            "max_tokens": 180,
        }

        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        return data["choices"][0]["message"]["content"].strip()
