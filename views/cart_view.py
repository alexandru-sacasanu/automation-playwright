class CartView:
    def __init__(self, page):
        self.page = page
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator("#checkout")

    def is_loaded(self):
        self.page.locator(".cart_list").wait_for()
        return self

    def item_count(self):
        return self.cart_items.count()

    def item_names(self):
        return self.cart_items.locator(".inventory_item_name").all_inner_texts()

    def checkout(self):
        self.checkout_button.click()
        return self
