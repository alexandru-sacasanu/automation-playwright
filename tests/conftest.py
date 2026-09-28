import base64
import re
import sys
from pathlib import Path

import pytest
import pytest_html

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import Config
from flows.auth_flow import AuthFlow
from flows.shopping_flow import ShoppingFlow
from flows.checkout_flow import CheckoutFlow
from views.login_view import LoginView

STANDARD_USER = Config.STANDARD_USER
LOCKED_USER = Config.LOCKED_USER
PASSWORD = Config.PASSWORD


@pytest.fixture(autouse=True)
def _set_default_timeout(page):
    page.set_default_timeout(Config.DEFAULT_TIMEOUT_MS)


@pytest.fixture
def login_view(page):
    return LoginView(page).goto()


@pytest.fixture
def auth_flow(page):
    return AuthFlow(page)


@pytest.fixture
def inventory_view(page):
    """Logged-in inventory view, ready for shopping."""
    return AuthFlow(page).login_as_standard_user()


@pytest.fixture
def shopping_flow(inventory_view, page):
    return ShoppingFlow(page)


@pytest.fixture
def checkout_flow(page):
    return CheckoutFlow(page)


def pytest_html_report_title(report):
    report.title = "Automation Suite — SauceDemo"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    page = item.funcargs.get("page")
    extras = getattr(report, "extras", [])

    if report.failed and page is not None:
        try:
            screenshot_b64 = base64.b64encode(page.screenshot()).decode("utf-8")
            extras.append(pytest_html.extras.image(screenshot_b64, mime_type="image/png"))
        except Exception:
            pass

        # pytest-playwright writes the trace zip during fixture teardown, which
        # runs after this hook, so the file won't exist yet — link it anyway,
        # it'll be there by the time the report is opened.
        trace_dir_name = re.sub(r"[^A-Za-z0-9]+", "-", item.nodeid).strip("-").lower()
        trace_path = Path("traces") / trace_dir_name / "trace.zip"
        extras.append(pytest_html.extras.url(str(trace_path), name="Playwright trace"))

    report.extras = extras
