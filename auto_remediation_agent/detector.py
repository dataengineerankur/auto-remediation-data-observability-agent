"""Schema drift detector for the auto-remediation agent.

This module provides a simple file-based schema drift detector that compares
JSON schema snapshots and returns differences such as added, removed, or
changed columns.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


class SchemaDriftDetector:
    """Detects schema drift by comparing current and previous schema snapshots.

    Schemas are expected to be JSON mappings of column names to data types.
    """

    def __init__(self, current_schema_path: Path, previous_schema_path: Path) -> None:
        self.current_schema_path = Path(current_schema_path)
        self.previous_schema_path = Path(previous_schema_path)

    def _load_schema(self, path: Path) -> Dict[str, Any]:
        """Load a schema JSON file from disk."""
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def detect(self) -> Optional[Dict[str, Dict[str, Any]]]:
        """Detect schema drift.

        Returns a dictionary keyed by column names with information about the
        type of change (added, removed, type_change) and old/new data types.
        Returns None if no drift is detected.
        """
        current_schema = self._load_schema(self.current_schema_path)
        previous_schema = self._load_schema(self.previous_schema_path)

        issues: Dict[str, Dict[str, Any]] = {}

        # Check for added or changed columns
        for column, dtype in current_schema.items():
            if column not in previous_schema:
                issues[column] = {"change_type": "added", "new_type": dtype}
            elif previous_schema[column] != dtype:
                issues[column] = {
                    "change_type": "type_change",
                    "old_type": previous_schema[column],
                    "new_type": dtype,
                }

        # Check for removed columns
        for column, dtype in previous_schema.items():
            if column not in current_schema:
                issues[column] = {"change_type": "removed", "old_type": dtype}

        return issues or None
