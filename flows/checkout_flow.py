import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import Config
from flows.auth_flow import AuthFlow
from flows.shopping_flow import ShoppingFlow
from views.checkout_view import CheckoutView


class CheckoutFlow:
    """
    Full purchase journey: login -> add items -> cart -> checkout.
    Chains AuthFlow + ShoppingFlow + CheckoutView so tests can call one method.
    """

    def __init__(self, page):
        self.page = page

    def buy_items(self, *product_names, first_name=None, last_name=None, postal_code=None):
        AuthFlow(self.page).login_as_standard_user()
        cart_view = ShoppingFlow(self.page).add_items(*product_names).go_to_cart()
        cart_view.checkout()

        checkout_view = CheckoutView(self.page)
        checkout_view.fill_info(
            first_name or Config.CHECKOUT_FIRST_NAME,
            last_name or Config.CHECKOUT_LAST_NAME,
            postal_code or Config.CHECKOUT_POSTAL_CODE,
        )
        return checkout_view

    def start_checkout_with_items(self, *product_names):
        """Stops right before filling checkout info, for validation-error tests."""
        AuthFlow(self.page).login_as_standard_user()
        cart_view = ShoppingFlow(self.page).add_items(*product_names).go_to_cart()
        cart_view.checkout()
        return CheckoutView(self.page)
