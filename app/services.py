from __future__ import annotations

import json

from app import conversation_hooks
from app.database import execute, fetch_one


def resolve_agent_id_by_twilio_number(twilio_number: str) -> int | None:
    row = fetch_one(
        """
        SELECT id FROM agents
        WHERE twilio_number = ? AND is_active = 1
        """,
        (twilio_number,),
    )
    return int(row["id"]) if row else None


def create_call_session(
    *,
    call_sid: str | None,
    direction: str,
    from_number: str,
    to_number: str,
    agent_id: int | None,
    status: str,
    provider: str,
) -> int:
    call_session_id = execute(
        """
        INSERT INTO call_sessions (call_sid, direction, from_number, to_number, agent_id, status, provider)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (call_sid, direction, from_number, to_number, agent_id, status, provider),
    )
    store_call_state_transition(
        call_session_id=call_session_id,
        from_state=None,
        to_state=status,
        source="session_created",
        metadata={"call_sid": call_sid, "direction": direction},
    )
    conversation_hooks.on_call_session_created(call_session_id=call_session_id, direction=direction)
    return call_session_id


def store_call_state_transition(
    *,
    call_session_id: int,
    from_state: str | None,
    to_state: str,
    source: str,
    metadata: dict | None = None,
) -> int:
    transition_id = execute(
        """
        INSERT INTO call_state_transitions (call_session_id, from_state, to_state, source, metadata_json)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            call_session_id,
            from_state,
            to_state,
            source,
            json.dumps(metadata or {}),
        ),
    )
    execute(
        """
        UPDATE call_sessions
        SET status = ?, updated_at = datetime('now')
        WHERE id = ?
        """,
        (to_state, call_session_id),
    )
    conversation_hooks.on_call_state_transition(
        call_session_id=call_session_id,
        to_state=to_state,
        source=source,
    )
    return transition_id


def get_call_session_by_id(call_session_id: int) -> dict:
    row = fetch_one("SELECT * FROM call_sessions WHERE id = ?", (call_session_id,))
    if not row:
        raise ValueError(f"Call session {call_session_id} not found")
    return dict(row)


def find_call_session_by_call_sid(call_sid: str) -> dict | None:
    row = fetch_one("SELECT * FROM call_sessions WHERE call_sid = ?", (call_sid,))
    return dict(row) if row else None
