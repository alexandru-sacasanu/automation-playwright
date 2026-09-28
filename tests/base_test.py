import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import Config
from flows.auth_flow import AuthFlow
from flows.shopping_flow import ShoppingFlow
from flows.checkout_flow import CheckoutFlow


class BaseTest:
    """Shared flow access and config for every test class."""

    config = Config

    def auth_flow(self, page):
        return AuthFlow(page)

    def shopping_flow(self, page):
        return ShoppingFlow(page)

    def checkout_flow(self, page):
        return CheckoutFlow(page)
