class LLMOrchestratorAdapter:
    """Interface boundary for OpenAI realtime/voice orchestration."""

    async def start_session(self, system_prompt: str, tools: list[dict]) -> dict:
        # NOTE: intentionally minimal foundation hook.
        return {"session_id": "stub-session", "system_prompt": system_prompt, "tools": tools}
