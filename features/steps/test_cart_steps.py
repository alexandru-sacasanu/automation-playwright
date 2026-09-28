import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pytest_bdd import scenarios, given, when, then, parsers

from flows.auth_flow import AuthFlow
from flows.shopping_flow import ShoppingFlow

scenarios("../cart.feature")


@given("I am logged in as the standard user", target_fixture="shopping_flow")
def logged_in_as_standard_user(page):
    AuthFlow(page).login_as_standard_user()
    return ShoppingFlow(page)


@when(parsers.parse('I add "{product}" to the cart'))
def add_to_cart(shopping_flow, product):
    shopping_flow.add_items(product)


@when(parsers.parse('I remove "{product}" from the cart'))
def remove_from_cart(shopping_flow, product):
    shopping_flow.remove_item(product)


@then(parsers.parse('the cart badge should show "{count}"'))
def cart_badge_shows(shopping_flow, count):
    assert shopping_flow.cart_count() == int(count)
