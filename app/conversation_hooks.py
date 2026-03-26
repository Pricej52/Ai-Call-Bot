from __future__ import annotations


def on_call_session_created(*, call_session_id: int, direction: str) -> None:
    """Placeholder hook for conversation engine bootstrap."""


def on_call_state_transition(*, call_session_id: int, to_state: str, source: str) -> None:
    """Placeholder hook for future conversation engine event ingestion."""
