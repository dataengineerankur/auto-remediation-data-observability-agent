"""Script to run the auto-remediation agent on sample data."""

from pathlib import Path

from auto_remediation_agent.agent import AutoRemediationAgent
from auto_remediation_agent.detector import SchemaDriftDetector
from auto_remediation_agent.remediator import SchemaRemediator


def main() -> None:
    """Run the AutoRemediationAgent on sample data."""
    base_dir = Path(__file__).resolve().parent
    current_schema_path = base_dir / "sample_data" / "current_schema.json"
    previous_schema_path = base_dir / "sample_data" / "previous_schema.json"
    transformation_script_path = base_dir / "scripts" / "transform.py"

    detector = SchemaDriftDetector(
        current_schema_path=current_schema_path,
        previous_schema_path=previous_schema_path,
    )
    remediator = SchemaRemediator(
        transformation_script_path=transformation_script_path,
    )
    agent = AutoRemediationAgent(detector=detector, remediator=remediator)

    remediation_result = agent.run()
    if remediation_result:
        print("Remediation recommendations:")
        for column, recommendation in remediation_result.items():
            print(f"- {column}: {recommendation}")
    else:
        print("No issues detected. No remediation needed.")


if __name__ == "__main__":
    main()
