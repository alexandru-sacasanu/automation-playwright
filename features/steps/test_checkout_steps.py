import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pytest_bdd import scenarios, given, when, then, parsers

from config import Config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

scenarios("../checkout.feature")


@given("I am logged in as the standard user", target_fixture="inventory_page")
def logged_in_as_standard_user(page):
    LoginPage(page).goto().login(Config.STANDARD_USER, Config.PASSWORD)
    return InventoryPage(page).is_loaded()


@given(parsers.parse('I have added "{product_a}" and "{product_b}" to the cart'))
def add_two_products(inventory_page, product_a, product_b):
    inventory_page.add_to_cart(product_a)
    inventory_page.add_to_cart(product_b)


@given("I go to the cart page", target_fixture="cart_page")
def go_to_cart_page(inventory_page, page):
    inventory_page.open_cart()
    return CartPage(page).is_loaded()


@when("I proceed to checkout", target_fixture="checkout_page")
def proceed_to_checkout(cart_page, page):
    cart_page.checkout()
    return CheckoutPage(page)


@when(parsers.re(
    r'I fill in checkout info with first name "(?P<first_name>.*?)", '
    r'last name "(?P<last_name>.*?)", postal code "(?P<postal_code>.*?)"'
))
def fill_checkout_info(checkout_page, first_name, last_name, postal_code):
    checkout_page.fill_info(first_name, last_name, postal_code)


@when("I finish the checkout")
def finish_checkout(checkout_page):
    checkout_page.finish()


@then(parsers.parse('I should see an order confirmation containing "{text}"'))
def see_confirmation(checkout_page, text):
    assert text in checkout_page.confirmation_text()


@then("I should see a checkout error")
def see_checkout_error(checkout_page):
    assert checkout_page.error_message.is_visible()
