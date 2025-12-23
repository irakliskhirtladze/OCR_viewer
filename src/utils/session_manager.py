"""Centralized session state manager using the Memento pattern."""
import json
import os
from pathlib import Path
from datetime import datetime

from utils.file_utils import get_app_data_dir


class SessionManager:
    """Collects and restores state from registered components."""

    def __init__(self):
        self._components: dict[str, object] = {}
        self._session_file = get_app_data_dir() / "session.json"

    def register(self, name: str, component: object):
        """Register a component that has get_memento/set_memento methods."""
        if not hasattr(component, 'get_memento') or not hasattr(component, 'set_memento'):
            raise ValueError(f"Component '{name}' must have get_memento and set_memento methods")
        self._components[name] = component

    def collect_state(self) -> dict:
        """Gather mementos from all registered components."""
        state = {
            "version": 1,
            "saved_at": datetime.now().isoformat(),
        }
        for name, component in self._components.items():
            state[name] = component.get_memento()
        return state

    def restore_state(self, state: dict):
        """Push mementos back to registered components."""
        for name, component in self._components.items():
            if name in state:
                component.set_memento(state[name])

    def save(self):
        """Save current state to disk with atomic write."""
        state = self.collect_state()
        temp_path = self._session_file.with_suffix(".json.tmp")

        # Write to temp file first
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

        # Atomic rename
        os.replace(temp_path, self._session_file)

    def load(self) -> dict | None:
        """Load state from disk. Returns None if no session exists."""
        if not self._session_file.exists():
            return None
        try:
            with open(self._session_file, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def has_saved_session(self) -> bool:
        """Check if a saved session exists."""
        return self._session_file.exists()

    def clear(self):
        """Delete saved session."""
        if self._session_file.exists():
            self._session_file.unlink()
