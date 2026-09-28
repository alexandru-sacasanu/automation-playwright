"""Render reports/run_log.json into a static HTML report."""
import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = ROOT / "reports" / "run_log.json"
OUTPUT_PATH = ROOT / "reports" / "index.html"


def build():
    run = json.loads(LOG_PATH.read_text())
    env = Environment(loader=FileSystemLoader(str(ROOT / "templates")))
    template = env.get_template("report.html.j2")
    OUTPUT_PATH.write_text(template.render(run=run))
    print(f"Report written to {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
