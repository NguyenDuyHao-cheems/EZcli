"""JSON-based local command history storage."""

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from ezcli.domain.models import ExecutionStatus, HistoryEntry, SafetyLevel


class HistoryStore:
    """Store command history in a local JSON file."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def save(self, entry: HistoryEntry) -> None:
        """Append one history entry to the JSON history file."""
        entries = self.load()
        entries.append(entry)

        self._path.parent.mkdir(parents=True, exist_ok=True)
        serialized = [
            {
                **asdict(item),
                "timestamp": item.timestamp.isoformat(),
                "safety": item.safety.value,
                "status": item.status.value,
            }
            for item in entries
        ]

        self._path.write_text(
            json.dumps(serialized, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def load(self) -> list[HistoryEntry]:
        """Load history entries, returning an empty list if no file exists."""
        if not self._path.exists():
            return []

        raw_entries = json.loads(self._path.read_text(encoding="utf-8"))

        return [
            HistoryEntry(
                prompt=item["prompt"],
                command=item["command"],
                timestamp=datetime.fromisoformat(item["timestamp"]),
                safety=SafetyLevel(item["safety"]),
                status=ExecutionStatus(item["status"]),
                exit_code=item.get("exit_code"),
            )
            for item in raw_entries
        ]
