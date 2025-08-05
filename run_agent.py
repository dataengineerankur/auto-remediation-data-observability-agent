#!/usr/bin/env python3

"""Run the auto-remediation agent with arbitrary schema files.

This script acts as a CLI wrapper for the AutoRemediationAgent. It accepts paths
 to a previous schema JSON file, a current schema JSON file and a transformation
 script. It then runs the agent and prints remediation recommendations.
"""

from pathlib import Path
import argparse

from auto_remediation_agent.agent import AutoRemediationAgent
from auto_remediation_agent.detector import SchemaDriftDetector
from auto_remediation_agent.remediator import SchemaRemediator


def run(previous_schema: Path, current_schema: Path, script_path: Path) -> None:
    """Run the agent with the given schema and script paths."""
    detector = SchemaDriftDetector(
        current_schema_path=current_schema,
        previous_schema_path=previous_schema,
    )
    remediator = SchemaRemediator(transformation_script_path=script_path)
    agent = AutoRemediationAgent(detector=detector, remediator=remediator)
    remediation_result = agent.run()
    if remediation_result:
        print("Remediation recommendations:")
        for column, recommendation in remediation_result.items():
            print(f"{column}: {recommendation}")
    else:
        print("No issues detected. No remediation needed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the auto-remediation agent with schema files."
    )
    default_base = Path(__file__).resolve().parent
    parser.add_argument(
        "--previous-schema",
        type=str,
        default=str(default_base / "sample_data" / "previous_schema.json"),
        help="Path to the previous schema JSON file.",
    )
    parser.add_argument(
        "--current-schema",
        type=str,
        default=str(default_base / "sample_data" / "current_schema.json"),
        help="Path to the current schema JSON file.",
    )
    parser.add_argument(
        "--script",
        type=str,
        default=str(default_base / "scripts" / "transform.py"),
        help="Path to the transformation script to update.",
    )
    args = parser.parse_args()
    run(Path(args.previous_schema), Path(args.current_schema), Path(args.script))
