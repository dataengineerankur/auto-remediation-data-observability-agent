"""Schema remediation logic for the auto-remediation agent.

This module contains a simplistic remediator that suggests modifications
for a transformation script based on detected schema drift. In a real system,
this would generate code changes and potentially submit pull requests or
execute rollbacks.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .llm import call_llm


class SchemaRemediator:
    """Remediates schema drift by suggesting updates to a transformation script."""

    def __init__(self, transformation_script_path: Path) -> None:
        self.transformation_script_path = Path(transformation_script_path)

    def remediate(self, issues: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        """Generate remediation suggestions for each issue using an LLM.

        This method reads the existing transformation script (if it exists) and
        constructs a prompt describing the schema drift for each column. It then
        calls the LLM via :func:`call_llm` to generate a remediation suggestion.

        Args:
            issues: Mapping of column names to metadata about the detected
                change (e.g., change_type, new_type, old_type).

        Returns:
            A dictionary mapping each column to an LLM‑generated suggestion.
        """
        script_text = ""
        if self.transformation_script_path.exists():
            script_text = self.transformation_script_path.read_text(encoding="utf-8")

        recommendations: Dict[str, str] = {}
        for column, change in issues.items():
            change_type = change.get("change_type")
            prompt_lines = [
                "You are an assistant that helps update data transformation scripts based on schema drift.",
                f"The current transformation script is:\n{script_text}",
                f"The column '{column}' has changed with change_type='{change_type}'.",
            ]
            if change_type == "added":
                prompt_lines.append(
                    "It is a new column that exists in the current schema but not in the previous schema."
                )
            elif change_type == "removed":
                prompt_lines.append(
                    "This column has been removed from the current schema but was present previously."
                )
            elif change_type == "type_change":
                new_type = change.get("new_type")
                old_type = change.get("old_type")
                prompt_lines.append(
                    f"The column's type changed from {old_type} to {new_type}."
                )
            prompt_lines.append(
                "Suggest a concise code modification to the transformation script to handle this change."
            )
            prompt = "\n".join(prompt_lines)
            try:
                suggestion = call_llm(prompt, model_name="llama3-70b-8192", temperature=0)
            except Exception as exc:
                # Fall back to a default suggestion on error
                suggestion = f"[LLM error: {exc}]"
            recommendations[column] = suggestion.strip()

        return recommendations
