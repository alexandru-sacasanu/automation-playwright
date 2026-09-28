import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pytest_bdd import scenarios, given, when, then, parsers

from config import Config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

scenarios("../cart.feature")


@given("I am logged in as the standard user", target_fixture="inventory_page")
def logged_in_as_standard_user(page):
    LoginPage(page).goto().login(Config.STANDARD_USER, Config.PASSWORD)
    return InventoryPage(page).is_loaded()


@when(parsers.parse('I add "{product}" to the cart'))
def add_to_cart(inventory_page, product):
    inventory_page.add_to_cart(product)


@when(parsers.parse('I remove "{product}" from the cart'))
def remove_from_cart(inventory_page, product):
    inventory_page.remove_from_cart(product)


@then(parsers.parse('the cart badge should show "{count}"'))
def cart_badge_shows(inventory_page, count):
    assert inventory_page.cart_count() == int(count)
