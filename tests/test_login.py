import pytest

from tests.conftest import STANDARD_USER, LOCKED_USER, PASSWORD


def test_valid_login_shows_inventory(login_page, page):
    login_page.login(STANDARD_USER, PASSWORD)
    assert page.locator(".inventory_list").is_visible()


def test_locked_out_user_sees_error(login_page):
    login_page.login(LOCKED_USER, PASSWORD)
    assert login_page.error_message.is_visible()
    assert "locked out" in login_page.error_message.inner_text().lower()


def test_invalid_password_sees_error(login_page):
    login_page.login(STANDARD_USER, "wrong_password")
    assert login_page.error_message.is_visible()


@pytest.mark.parametrize("username,password", [("", ""), (STANDARD_USER, "")])
def test_empty_credentials_blocked(login_page, username, password):
    login_page.login(username, password)
    assert login_page.error_message.is_visible()
