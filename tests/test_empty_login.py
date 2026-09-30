from playwright.sync_api import Page

from pages.login_page import LoginPage


def test_empty_login(page: Page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login_button.click()

    error_message = login_page.get_error_message()
    assert "Username is required" in error_message, (
        f"Expected a required-fields error, got: {error_message}"
    )
