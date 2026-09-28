# Web Automation Demo

A Playwright automation script that logs into [saucedemo.com](https://www.saucedemo.com), adds items to the cart, and completes checkout — then generates a static HTML report of the run (steps, timings, screenshots).

## Stack

- **Python + Playwright** — browser automation
- **Jinja2** — renders the structured run log into a static HTML report
- **GitHub Actions** — runs the automation on a schedule and publishes the report
- **Netlify** — hosts the published report

## Run locally

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium

python scripts/run_automation.py   # runs the automation, writes reports/run_log.json
python scripts/build_report.py     # renders reports/index.html
open reports/index.html
```

## Project structure

```
scripts/
  run_automation.py   # Playwright script + structured step logger
  build_report.py     # renders run_log.json -> reports/index.html
templates/
  report.html.j2       # report template
reports/
  run_log.json          # structured run log (generated)
  index.html             # published report (generated)
  screenshots/            # per-step screenshots (generated)
```
