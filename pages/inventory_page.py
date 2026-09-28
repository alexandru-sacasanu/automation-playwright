class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.inventory_list = page.locator(".inventory_list")
        self.cart_link = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")

    def is_loaded(self):
        self.inventory_list.wait_for()
        return self

    def add_to_cart(self, product_name):
        item = self.page.locator(".inventory_item", has_text=product_name)
        item.locator("button", has_text="Add to cart").click()
        return self

    def remove_from_cart(self, product_name):
        item = self.page.locator(".inventory_item", has_text=product_name)
        item.locator("button", has_text="Remove").click()
        return self

    def cart_count(self):
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())

    def open_cart(self):
        self.cart_link.click()
        return self
