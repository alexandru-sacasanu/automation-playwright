import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from views.inventory_view import InventoryView
from views.cart_view import CartView


class ShoppingFlow:
    """Chains InventoryView -> CartView for cart-building operations."""

    def __init__(self, page):
        self.page = page
        self.inventory_view = InventoryView(page)

    def add_items(self, *product_names):
        for name in product_names:
            self.inventory_view.add_to_cart(name)
        return self

    def remove_item(self, product_name):
        self.inventory_view.remove_from_cart(product_name)
        return self

    def cart_count(self):
        return self.inventory_view.cart_count()

    def go_to_cart(self):
        self.inventory_view.open_cart()
        return CartView(self.page).is_loaded()
