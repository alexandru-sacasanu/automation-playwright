import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import Config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

STANDARD_USER = Config.STANDARD_USER
LOCKED_USER = Config.LOCKED_USER
PASSWORD = Config.PASSWORD


@pytest.fixture
def login_page(page):
    page.set_default_timeout(Config.DEFAULT_TIMEOUT_MS)
    return LoginPage(page).goto()


@pytest.fixture
def logged_in_page(page):
    """Returns an InventoryPage after logging in as the standard user."""
    page.set_default_timeout(Config.DEFAULT_TIMEOUT_MS)
    LoginPage(page).goto().login(STANDARD_USER, PASSWORD)
    return InventoryPage(page).is_loaded()


@pytest.fixture
def inventory_page(logged_in_page):
    return logged_in_page


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)
