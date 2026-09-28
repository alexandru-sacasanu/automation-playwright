# Web Automation Test Suite

A Playwright + pytest test suite for [saucedemo.com](https://www.saucedemo.com), using Views (Page Object Model) and Flows (chained multi-view journeys). Covers login, cart, and checkout, and publishes an HTML report via pytest-html.

## Stack

- **Python + Playwright + pytest** — test framework
- **pytest-playwright** — browser fixtures, `--headed`/`--slowmo` support
- **Views** (`views/`) — one class per page, encapsulates locators/actions (Page Object Model)
- **Flows** (`flows/`) — chains multiple views into a full user journey (e.g. login → add to cart → checkout); tests call one flow method and assert
- **pytest-html** — self-contained HTML report of the run
- **pytest-bdd** — Cucumber-style Gherkin `.feature` files with Python step definitions
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

# run a suite by marker
pytest -m login                 # all login tests
pytest -m cart                  # all cart tests
pytest -m checkout              # all checkout tests
pytest -m smoke                 # critical-path tests only
pytest -m regression            # broader coverage

# watch it run in a real browser
pytest --headed --slowmo 500

# run only the Cucumber/Gherkin scenarios
pytest features/
```

## Configuration

Test settings (base URL, credentials, timeouts) live in [config.py](config.py) and can be overridden via environment variables, e.g.:

```bash
BASE_URL=https://www.saucedemo.com STANDARD_USER=standard_user pytest
```

## Views and Flows

- A **view** wraps one page's locators and actions (e.g. `CheckoutView.fill_info(...)`).
- A **flow** chains several views into one journey a test can call in a single line, e.g.:

```python
checkout_view = checkout_flow.buy_items("Sauce Labs Backpack", "Sauce Labs Bike Light")
assert "Total" in checkout_view.total_text()
```

`CheckoutFlow.buy_items` internally logs in (`AuthFlow`), adds items and opens the cart (`ShoppingFlow`), starts checkout, and fills the checkout form — the test only calls the flow and asserts on the result.

## Suites (markers)

Defined in [pytest.ini](pytest.ini):

- `login`, `cart`, `checkout` — feature suites
- `smoke` — critical-path tests, safe to run on every push
- `regression` — broader coverage, run on a schedule or before release

Open `reports/pytest_report.html` in a browser to view the report.

## Project structure

```
config.py                # test settings (base URL, credentials, timeouts)
views/                  # Page Object Model — one class per page
  login_view.py
  inventory_view.py
  cart_view.py
  checkout_view.py
flows/                   # chains views into full user journeys
  auth_flow.py            # login
  shopping_flow.py        # add/remove cart items
  checkout_flow.py        # login -> cart -> checkout, end to end
tests/
  conftest.py            # shared fixtures (exposes flows to tests)
  base_test.py           # BaseTest class, flow access for test classes
  test_login.py
  test_cart.py
  test_checkout.py
features/                 # Cucumber-style Gherkin scenarios (pytest-bdd)
  login.feature
  cart.feature
  checkout.feature
  steps/
    test_login_steps.py
    test_cart_steps.py
    test_checkout_steps.py
pytest.ini                # pytest config, markers, default report output path
reports/
  pytest_report.html        # generated test report (published to Netlify)
```
