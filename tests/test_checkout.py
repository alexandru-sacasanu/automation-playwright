import pytest

from tests.base_test import BaseTest

PRODUCT_A = "Sauce Labs Backpack"
PRODUCT_B = "Sauce Labs Bike Light"


@pytest.mark.checkout
class TestCheckout(BaseTest):

    @pytest.mark.smoke
    def test_full_checkout_flow_completes(self, checkout_flow):
        checkout_view = checkout_flow.buy_items(PRODUCT_A, PRODUCT_B)
        assert "Total" in checkout_view.total_text()

        checkout_view.finish()
        assert "Thank you" in checkout_view.confirmation_text()

    @pytest.mark.regression
    def test_checkout_requires_first_name(self, checkout_flow):
        checkout_view = checkout_flow.start_checkout_with_items(PRODUCT_A, PRODUCT_B)
        checkout_view.fill_info("", "Demo", "94107")
        assert checkout_view.error_message.is_visible()

    @pytest.mark.regression
    def test_checkout_requires_postal_code(self, checkout_flow):
        checkout_view = checkout_flow.start_checkout_with_items(PRODUCT_A, PRODUCT_B)
        checkout_view.fill_info("Alex", "Demo", "")
        assert checkout_view.error_message.is_visible()
