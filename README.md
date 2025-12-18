# CSV Profiler

Generate a profiling report for a CSV file using a CLI or a Streamlit web app.
The project analyzes CSV data and produces summary reports in JSON and Markdown formats.

## Features
- CLI tool to generate profiling reports
- Outputs JSON and Markdown files
- Streamlit GUI to upload CSV files
- Preview reports and download outputs

## Setup
This project requires **Python 3.11** and uses `requirements.txt`.

in bash
uv venv -p 3.11
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate    # Windows

uv pip install -r requirements.txt

## RunCLI
    Because the source code lives in src/, you must set PYTHONPATH.
    # Mac/Linux: export PYTHONPATH=src
    # Windows: $env:PYTHONPATH="src"
    uv run python -m csv_profiler.cli data/sample.csv --out-dir outputs

## Run GUI (Streamlit)
The Streamlit app is located at the project root (app.py).
    # Mac/Linux: export PYTHONPATH=src
    # Windows: $env:PYTHONPATH="src"
    uv run streamlit run app.py

## Output Files
The CLI generates:
- outputs/report.json
- outputs/report.md

The Streamlit app allows you to:
- Preview the report
- Download JSON and Markdown files