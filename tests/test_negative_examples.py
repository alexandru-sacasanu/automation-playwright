"""
Intentionally failing tests, used to demonstrate what a red run looks
like in the HTML report (wrong credentials, wrong product name, wrong
assertions). Not meant to represent real product bugs.
"""
import pytest

from tests.base_test import BaseTest

BAD_USERNAME = "definitely_not_a_real_user"
NONEXISTENT_PRODUCT = "Sauce Labs Flying Carpet"


@pytest.mark.regression
class TestNegativeExamples(BaseTest):

    def test_login_with_made_up_username_fails(self, auth_flow):
        """Fails: made-up username never shows the inventory list."""
        login_view = auth_flow.attempt_login(BAD_USERNAME, "secret_sauce")
        assert login_view.page.locator(".inventory_list").is_visible()

    def test_adding_nonexistent_product_raises(self, shopping_flow):
        """Fails: product name doesn't exist on the page, locator times out."""
        shopping_flow.add_items(NONEXISTENT_PRODUCT)
        assert shopping_flow.cart_count() == 1

    def test_cart_count_wrong_expectation(self, shopping_flow):
        """Fails: adds 1 item but asserts on 5 — wrong expected value."""
        shopping_flow.add_items("Sauce Labs Backpack")
        assert shopping_flow.cart_count() == 5

    def test_checkout_total_wrong_text(self, checkout_flow):
        """Fails: summary label never contains this literal string."""
        checkout_view = checkout_flow.buy_items("Sauce Labs Backpack")
        assert "Grand Total: $999.99" in checkout_view.total_text()
