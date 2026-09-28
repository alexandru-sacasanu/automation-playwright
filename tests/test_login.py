import pytest

from tests.base_test import BaseTest
from tests.conftest import STANDARD_USER, LOCKED_USER, PASSWORD


@pytest.mark.login
class TestLogin(BaseTest):

    @pytest.mark.smoke
    def test_valid_login_shows_inventory(self, auth_flow, page):
        auth_flow.login(STANDARD_USER, PASSWORD)
        assert page.locator(".inventory_list").is_visible()

    @pytest.mark.regression
    def test_locked_out_user_sees_error(self, auth_flow):
        login_view = auth_flow.attempt_login(LOCKED_USER, PASSWORD)
        assert login_view.error_message.is_visible()
        assert "locked out" in login_view.error_message.inner_text().lower()

    @pytest.mark.regression
    def test_invalid_password_sees_error(self, auth_flow):
        login_view = auth_flow.attempt_login(STANDARD_USER, "wrong_password")
        assert login_view.error_message.is_visible()

    @pytest.mark.regression
    @pytest.mark.parametrize("username,password", [("", ""), (STANDARD_USER, "")])
    def test_empty_credentials_blocked(self, auth_flow, username, password):
        login_view = auth_flow.attempt_login(username, password)
        assert login_view.error_message.is_visible()
