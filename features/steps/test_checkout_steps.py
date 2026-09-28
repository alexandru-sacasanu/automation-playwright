import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pytest_bdd import scenarios, given, when, then, parsers

from flows.checkout_flow import CheckoutFlow

scenarios("../checkout.feature")


@given("I am logged in as the standard user", target_fixture="checkout_flow")
def logged_in_as_standard_user(page):
    return CheckoutFlow(page)


@given(parsers.parse('I have added "{product_a}" and "{product_b}" to the cart'), target_fixture="products")
def remember_products(product_a, product_b):
    return (product_a, product_b)


@given("I go to the cart page", target_fixture="checkout_view")
def go_to_cart_and_checkout(checkout_flow, products):
    return checkout_flow.start_checkout_with_items(*products)


@when("I proceed to checkout")
def proceed_to_checkout():
    pass  # already on the checkout page from the Background step


@when(parsers.re(
    r'I fill in checkout info with first name "(?P<first_name>.*?)", '
    r'last name "(?P<last_name>.*?)", postal code "(?P<postal_code>.*?)"'
))
def fill_checkout_info(checkout_view, first_name, last_name, postal_code):
    checkout_view.fill_info(first_name, last_name, postal_code)


@when("I finish the checkout")
def finish_checkout(checkout_view):
    checkout_view.finish()


@then(parsers.parse('I should see an order confirmation containing "{text}"'))
def see_confirmation(checkout_view, text):
    assert text in checkout_view.confirmation_text()


@then("I should see a checkout error")
def see_checkout_error(checkout_view):
    assert checkout_view.error_message.is_visible()
