from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def test_add_to_cart(page: Page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(page)
    inventory_page.add_to_cart("Sauce Labs Backpack")

    expect(inventory_page.cart_badge).to_have_text("1")
