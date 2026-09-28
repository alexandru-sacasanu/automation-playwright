import pytest

from tests.base_test import BaseTest

PRODUCT_A = "Sauce Labs Backpack"
PRODUCT_B = "Sauce Labs Bike Light"


@pytest.mark.checkout
class TestCheckout(BaseTest):

    def _add_items_and_go_to_cart(self, inventory_page, cart_page):
        inventory_page.add_to_cart(PRODUCT_A)
        inventory_page.add_to_cart(PRODUCT_B)
        inventory_page.open_cart()
        cart_page.is_loaded()

    @pytest.mark.smoke
    def test_full_checkout_flow_completes(self, inventory_page, cart_page, checkout_page):
        self._add_items_and_go_to_cart(inventory_page, cart_page)
        cart_page.checkout()

        checkout_page.fill_info(
            self.config.CHECKOUT_FIRST_NAME,
            self.config.CHECKOUT_LAST_NAME,
            self.config.CHECKOUT_POSTAL_CODE,
        )
        assert "Total" in checkout_page.total_text()

        checkout_page.finish()
        assert "Thank you" in checkout_page.confirmation_text()

    @pytest.mark.regression
    def test_checkout_requires_first_name(self, inventory_page, cart_page, checkout_page):
        self._add_items_and_go_to_cart(inventory_page, cart_page)
        cart_page.checkout()

        checkout_page.fill_info("", "Demo", "94107")
        assert checkout_page.error_message.is_visible()

    @pytest.mark.regression
    def test_checkout_requires_postal_code(self, inventory_page, cart_page, checkout_page):
        self._add_items_and_go_to_cart(inventory_page, cart_page)
        cart_page.checkout()

        checkout_page.fill_info("Alex", "Demo", "")
        assert checkout_page.error_message.is_visible()
