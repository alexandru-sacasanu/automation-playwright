PRODUCT_A = "Sauce Labs Backpack"
PRODUCT_B = "Sauce Labs Bike Light"


def test_add_single_item_updates_badge(inventory_page):
    inventory_page.add_to_cart(PRODUCT_A)
    assert inventory_page.cart_count() == 1


def test_add_multiple_items_updates_badge(inventory_page):
    inventory_page.add_to_cart(PRODUCT_A)
    inventory_page.add_to_cart(PRODUCT_B)
    assert inventory_page.cart_count() == 2


def test_remove_item_updates_badge(inventory_page):
    inventory_page.add_to_cart(PRODUCT_A)
    inventory_page.add_to_cart(PRODUCT_B)
    inventory_page.remove_from_cart(PRODUCT_A)
    assert inventory_page.cart_count() == 1


def test_cart_page_lists_added_items(inventory_page, cart_page):
    inventory_page.add_to_cart(PRODUCT_A)
    inventory_page.add_to_cart(PRODUCT_B)
    inventory_page.open_cart()
    cart_page.is_loaded()

    assert cart_page.item_count() == 2
    assert set(cart_page.item_names()) == {PRODUCT_A, PRODUCT_B}
