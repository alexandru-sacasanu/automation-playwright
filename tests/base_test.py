import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import Config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class BaseTest:
    """Shared setup for page-object access and config in every test class."""

    config = Config

    def login_page(self, page):
        return LoginPage(page).goto()

    def inventory_page(self, page):
        return InventoryPage(page)

    def cart_page(self, page):
        return CartPage(page)

    def checkout_page(self, page):
        return CheckoutPage(page)

    def login_as_standard_user(self, page):
        self.login_page(page).login(self.config.STANDARD_USER, self.config.PASSWORD)
        return self.inventory_page(page).is_loaded()
