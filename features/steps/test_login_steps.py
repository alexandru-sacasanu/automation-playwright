import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pytest_bdd import scenarios, given, when, then, parsers

from pages.login_page import LoginPage

scenarios("../login.feature")


@given("I am on the login page", target_fixture="login_page")
def login_page(page):
    return LoginPage(page).goto()


@when(parsers.parse('I log in with username "{username}" and password "{password}"'))
def log_in(login_page, username, password):
    login_page.login(username, password)


@then("I should see the product inventory")
def see_inventory(page):
    assert page.locator(".inventory_list").is_visible()


@then(parsers.parse('I should see a login error containing "{text}"'))
def see_login_error_with_text(login_page, text):
    assert login_page.error_message.is_visible()
    assert text.lower() in login_page.error_message.inner_text().lower()


@then("I should see a login error")
def see_login_error(login_page):
    assert login_page.error_message.is_visible()
