import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import Config
from views.login_view import LoginView
from views.inventory_view import InventoryView


class AuthFlow:
    """Chains LoginView -> InventoryView for anything that starts with 'be logged in'."""

    def __init__(self, page):
        self.page = page

    def login(self, username, password):
        LoginView(self.page).goto().login(username, password)
        return self

    def login_as_standard_user(self):
        self.login(Config.STANDARD_USER, Config.PASSWORD)
        return InventoryView(self.page).is_loaded()

    def attempt_login(self, username, password):
        """Returns the LoginView itself, for asserting error states."""
        return LoginView(self.page).goto().login(username, password)
