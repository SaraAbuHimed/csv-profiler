from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

''' old write_markdown function
def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        # Title
        f.write("# CSV Profile Report\n\n")

        # Rows and columns
        f.write(f"**Rows:** {report['row_count']}\n\n")
        f.write("**Columns:** " + ", ".join(report["columns"]) + "\n\n")

        # Table header
        f.write("| Column | Missing |\n")
        f.write("|--------|---------|\n")

        # Table rows
        for column, count in report["missing"].items():
            f.write(f"| {column} | {count} |\n")
'''

def md_header(source: str) -> list[str]:
  lines = []
  lines.append("# CSV Profiling Report")
  lines.append(f"# {source}")
  lines.append(f"# {datetime.now().isoformat(timespec='seconds')}")
  return lines

def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = report["summary"]["rows"]

    with path.open("w", encoding="utf-8") as f:
        for line in md_header(report.get("source", "unknown")):
            f.write(line + "\n")
        f.write("\n")

        f.write("## Summary\n")
        f.write(f"- **Rows:** {report['summary']['rows']}\n")
        f.write(f"- **Columns:** {report['summary']['columns']}\n\n")

        f.write("## Columns Overview\n")
        f.write("| Column | Type | Missing % | Unique |\n")
        f.write("|--------|------|-----------|--------|\n")

        for col, col_report in report["columns"].items():
            missing = col_report.get("missing", 0)
            missing_pct = (missing / rows) if rows else 0.0
            unique = col_report.get("unique", 0)

            f.write(
                f"| {col} | {col_report['type']} | "
                f"{missing_pct:.2%} | {unique} |\n"
            )

        f.write("\n")

        f.write("## Column Details\n\n")

        for col, col_report in report["columns"].items():
            f.write(f"### {col}\n")

            if col_report["type"] == "number":
                f.write(f"- Min: {col_report.get('min')}\n")
                f.write(f"- Max: {col_report.get('max')}\n")
                f.write(f"- Mean: {col_report.get('mean')}\n")
            else:
                f.write("- Top values:\n")
                for value, count in col_report.get("top", []):
                    f.write(f"  - {value}: {count}\n")

            f.write("\n")

def render_markdown(report: dict) -> str:
    lines: list[str] = []

    lines.append("# CSV Profiling Report\n")
    lines.append(
        f"Generated: {datetime.now().isoformat(timespec='seconds')}\n"
    )

    lines.append("## Summary\n")
    lines.append(f"- Rows: **{report['n_rows']}**")
    lines.append(f"- Columns: **{report['n_cols']}**\n")

    lines.append("## Columns\n")
    lines.append("| name | type | missing | missing_pct | unique |")
    lines.append("| --- | --- | --- | --- | --- |")

    for col in report["columns"]:
        lines.append(
            f"| {col['name']} | {col['type']} | {col['missing']} | "
            f"{col['missing_pct']:.2f} | {col['unique']} |"
        )

    lines.append("\n## Notes\n")
    lines.append(
        "- Missing values are: `''`, `na`, `n/a`, `null`, `none`, `nan` "
        "(case-insensitive)"
    )

    return "\n".join(lines)
