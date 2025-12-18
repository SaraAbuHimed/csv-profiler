import json
import time
import typer
from pathlib import Path

from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown

app = typer.Typer()


@app.command(help="Profile a CSV file and write JSON + Markdown")
def profile(
    input_path: Path = typer.Argument(..., help="Input CSV file"),
    out_dir: Path = typer.Option(Path("outputs"), "--out-dir", help="Output folder"),
    report_name: str = typer.Option("report", "--report-name", help="Base name for outputs"),
    preview: bool = typer.Option(False, "--preview", help="Print a short summary"),
):
    start = time.perf_counter()

    try:
        rows = read_csv_rows(input_path)

        report = profile_rows(rows)

        markdown = render_markdown(report)

        out_dir.mkdir(parents=True, exist_ok=True)

        json_path = out_dir / f"{report_name}.json"
        json_path.write_text(
            json.dumps(report, indent=2),
            encoding="utf-8",
        )

        md_path = out_dir / f"{report_name}.md"
        md_path.write_text(markdown, encoding="utf-8")

        elapsed_ms = (time.perf_counter() - start) * 1000

        if preview:
            typer.echo(f"Rows: {report['n_rows']}, Columns: {report['n_cols']}")
            typer.echo(f"Time: {elapsed_ms:.2f} ms")

    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
