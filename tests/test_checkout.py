PRODUCT_A = "Sauce Labs Backpack"
PRODUCT_B = "Sauce Labs Bike Light"


def _add_items_and_go_to_cart(inventory_page, cart_page):
    inventory_page.add_to_cart(PRODUCT_A)
    inventory_page.add_to_cart(PRODUCT_B)
    inventory_page.open_cart()
    cart_page.is_loaded()


def test_full_checkout_flow_completes(inventory_page, cart_page, checkout_page):
    _add_items_and_go_to_cart(inventory_page, cart_page)
    cart_page.checkout()

    checkout_page.fill_info("Alex", "Demo", "94107")
    assert "Total" in checkout_page.total_text()

    checkout_page.finish()
    assert "Thank you" in checkout_page.confirmation_text()


def test_checkout_requires_first_name(inventory_page, cart_page, checkout_page):
    _add_items_and_go_to_cart(inventory_page, cart_page)
    cart_page.checkout()

    checkout_page.fill_info("", "Demo", "94107")
    assert checkout_page.error_message.is_visible()


def test_checkout_requires_postal_code(inventory_page, cart_page, checkout_page):
    _add_items_and_go_to_cart(inventory_page, cart_page)
    cart_page.checkout()

    checkout_page.fill_info("Alex", "Demo", "")
    assert checkout_page.error_message.is_visible()
