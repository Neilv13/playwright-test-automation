from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def test_login(page: Page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
