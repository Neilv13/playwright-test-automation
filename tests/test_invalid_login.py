from playwright.sync_api import Page

from pages.login_page import LoginPage


def test_invalid_login(page: Page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("invalid_user", "wrong_password")

    error_message = login_page.get_error_message()
    assert "do not match any user" in error_message, (
        f"Expected an invalid-credentials error, got: {error_message}"
    )
