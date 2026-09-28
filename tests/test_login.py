import pytest

from tests.base_test import BaseTest
from tests.conftest import STANDARD_USER, LOCKED_USER, PASSWORD


@pytest.mark.login
class TestLogin(BaseTest):

    @pytest.mark.smoke
    def test_valid_login_shows_inventory(self, login_page, page):
        login_page.login(STANDARD_USER, PASSWORD)
        assert page.locator(".inventory_list").is_visible()

    @pytest.mark.regression
    def test_locked_out_user_sees_error(self, login_page):
        login_page.login(LOCKED_USER, PASSWORD)
        assert login_page.error_message.is_visible()
        assert "locked out" in login_page.error_message.inner_text().lower()

    @pytest.mark.regression
    def test_invalid_password_sees_error(self, login_page):
        login_page.login(STANDARD_USER, "wrong_password")
        assert login_page.error_message.is_visible()

    @pytest.mark.regression
    @pytest.mark.parametrize("username,password", [("", ""), (STANDARD_USER, "")])
    def test_empty_credentials_blocked(self, login_page, username, password):
        login_page.login(username, password)
        assert login_page.error_message.is_visible()
