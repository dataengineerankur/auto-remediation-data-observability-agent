# Auto-Remediation Data Observability Agent

This repository contains a proof-of-concept agent that monitors for data pipeline / schema drift issues and automatically suggests remediation actions. It demonstrates how an AI agent can detect added, removed or type-changed columns and generate guidance for updating ETL scripts.

## Usage

1. Clone this repository and install the (minimal) dependencies:

   ```bash
   git clone https://github.com/dataengineerankur/auto-remediation-data-observability-agent.git
   cd auto-remediation-data-observability-agent
   pip install -r requirements.txt
   ```

2. Run the agent script against the example schema drift:

   ```bash
   python run_agent.py
   ```

   You should see output similar to:

   ```
   Remediation recommendations:
   - age: Cast or convert column 'age' to the new type 'float' in the transformation script.
   - email: Consider adding handling for new column 'email' in the transformation script.
   - name: Remove references to column 'name' from the transformation script.
   ```

3. To experiment with your own schemas, place your last known good schema in `sample_data/previous_schema.json` and the new schema in `sample_data/current_schema.json`, adjust `scripts/transform.py` to represent your transformation logic, and run the agent again.

## Contents

- **auto_remediation_agent/** – package containing the agent, detector and remediator classes.
- **sample_data/** – example JSON schema snapshots used for the demo (`previous_schema.json` and `current_schema.json`).
- **scripts/transform.py** – a simple transformation script referenced by the demo.
- **run_agent.py** – entry point that wires everything together and prints remediation suggestions.
- **requirements.txt** – Python dependencies (very minimal).

This project is a starting point; in a production system the remediation suggestions would be applied automatically via pull requests or integration with your orchestration platform.
