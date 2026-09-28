import sys
from pathlib import Path

import pytest

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
