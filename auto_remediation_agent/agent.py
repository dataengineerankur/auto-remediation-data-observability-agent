"""Main agent orchestration for auto-remediation."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from .detector import SchemaDriftDetector
from .remediator import SchemaRemediator


class AutoRemediationAgent:
    """Agent that monitors for data quality or pipeline issues and automatically remediates them."""

    def __init__(
        self,
        detector: SchemaDriftDetector,
        remediator: SchemaRemediator,
    ) -> None:
        self.detector = detector
        self.remediator = remediator
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self) -> Optional[Dict[str, Any]]:
        """Run the agent once. Detect issues and remediate if any.

        Returns a dictionary describing the remediation result or None if no issues were found.
        """
        self.logger.info("Running auto-remediation agent...")
        issues = self.detector.detect()
        if issues:
            self.logger.info("Issues detected: %s", issues)
            result = self.remediator.remediate(issues)
            self.logger.info("Remediation result: %s", result)
            return result
        else:
            self.logger.info("No issues detected.")
            return None


if __name__ == "__main__":
    # Example usage with simple file-based schema detector/remediator
    import json
    import pathlib

    # Paths to sample schema files for current and previous runs
    current_schema_path = pathlib.Path("sample_data/current_schema.json")
    previous_schema_path = pathlib.Path("sample_data/previous_schema.json")

    detector = SchemaDriftDetector(current_schema_path=current_schema_path, previous_schema_path=previous_schema_path)
    remediator = SchemaRemediator(transformation_script_path=pathlib.Path("scripts/transform.py"))

    agent = AutoRemediationAgent(detector=detector, remediator=remediator)
    remediation = agent.run()
    if remediation:
        print("Remediation applied:", remediation)
    else:
        print("No remediation needed.")
