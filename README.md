# Web Automation Test Suite

A Playwright + pytest test suite for [saucedemo.com](https://www.saucedemo.com), using the Page Object Model. Covers login, cart, and checkout flows, and publishes an HTML report via pytest-html.

## Stack

- **Python + Playwright + pytest** — test framework
- **pytest-playwright** — browser fixtures, `--headed`/`--slowmo` support
- **Page Object Model** — page classes in `pages/` encapsulate locators/actions
- **pytest-html** — self-contained HTML report of the run
- **GitHub Actions** — runs the suite on push and on a daily schedule
- **Netlify** — hosts the published report

## Setup

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Run the tests

```bash
pytest                          # headless, generates reports/pytest_report.html
pytest -v                       # verbose output
pytest tests/test_login.py      # run one file
pytest -k "checkout"            # run tests matching a keyword

# watch it run in a real browser
pytest --headed --slowmo 500
```

Open `reports/pytest_report.html` in a browser to view the report.

## Project structure

```
pages/                  # Page Object Model
  login_page.py
  inventory_page.py
  cart_page.py
  checkout_page.py
tests/
  conftest.py            # shared fixtures (login, page objects)
  test_login.py
  test_cart.py
  test_checkout.py
pytest.ini                # pytest config, default report output path
reports/
  pytest_report.html        # generated test report (published to Netlify)
```
