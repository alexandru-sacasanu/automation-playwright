import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from pytest_bdd import scenarios, given, when, then, parsers

from flows.auth_flow import AuthFlow

scenarios("../login.feature")


@given("I am on the login page", target_fixture="auth_flow")
def on_login_page(page):
    return AuthFlow(page)


@when(parsers.parse('I log in with username "{username}" and password "{password}"'), target_fixture="login_view")
def log_in(auth_flow, username, password):
    return auth_flow.attempt_login(username, password)


@then("I should see the product inventory")
def see_inventory(page):
    assert page.locator(".inventory_list").is_visible()


@then(parsers.parse('I should see a login error containing "{text}"'))
def see_login_error_with_text(login_view, text):
    assert login_view.error_message.is_visible()
    assert text.lower() in login_view.error_message.inner_text().lower()


@then("I should see a login error")
def see_login_error(login_view):
    assert login_view.error_message.is_visible()
