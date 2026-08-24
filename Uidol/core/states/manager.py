"""
In-memory conversation state manager.
Used for multi-step flows (deploy userbot, etc).
States are never persisted to disk for security.
"""

from typing import Any, Dict, Optional
from dataclasses import dataclass, field
import time


@dataclass
class UserState:
    name: str
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None


class StateManager:
    def __init__(self):
        self._states: Dict[int, UserState] = {}

    def set(
        self,
        user_id: int,
        name: str,
        data: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None,
    ) -> None:
        expires = (time.time() + ttl) if ttl else None
        self._states[user_id] = UserState(
            name=name,
            data=data or {},
            expires_at=expires,
        )

    def get(self, user_id: int) -> Optional[UserState]:
        state = self._states.get(user_id)
        if not state:
            return None
        if state.expires_at and time.time() > state.expires_at:
            self.clear(user_id)
            return None
        return state

    def update_data(self, user_id: int, **kwargs) -> None:
        state = self.get(user_id)
        if state:
            state.data.update(kwargs)

    def clear(self, user_id: int) -> None:
        self._states.pop(user_id, None)

    def is_in(self, user_id: int, name: str) -> bool:
        state = self.get(user_id)
        return state is not None and state.name == name


# Global instance
states = StateManager()
