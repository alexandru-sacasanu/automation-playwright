import pytest

from tests.base_test import BaseTest

PRODUCT_A = "Sauce Labs Backpack"
PRODUCT_B = "Sauce Labs Bike Light"


@pytest.mark.cart
class TestCart(BaseTest):

    @pytest.mark.smoke
    def test_add_single_item_updates_badge(self, shopping_flow):
        shopping_flow.add_items(PRODUCT_A)
        assert shopping_flow.cart_count() == 1

    @pytest.mark.regression
    def test_add_multiple_items_updates_badge(self, shopping_flow):
        shopping_flow.add_items(PRODUCT_A, PRODUCT_B)
        assert shopping_flow.cart_count() == 2

    @pytest.mark.regression
    def test_remove_item_updates_badge(self, shopping_flow):
        shopping_flow.add_items(PRODUCT_A, PRODUCT_B).remove_item(PRODUCT_A)
        assert shopping_flow.cart_count() == 1

    @pytest.mark.regression
    def test_cart_page_lists_added_items(self, shopping_flow):
        cart_view = shopping_flow.add_items(PRODUCT_A, PRODUCT_B).go_to_cart()

        assert cart_view.item_count() == 2
        assert set(cart_view.item_names()) == {PRODUCT_A, PRODUCT_B}
