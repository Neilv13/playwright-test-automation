from playwright.sync_api import Page


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_badge = page.locator(".shopping_cart_badge")

    def add_to_cart(self, product_name: str):
        item = self.page.locator(".inventory_item").filter(has_text=product_name)
        item.get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, product_name: str):
        item = self.page.locator(".inventory_item").filter(has_text=product_name)
        item.get_by_role("button", name="Remove").click()

    def cart_count(self) -> str:
        return self.cart_badge.inner_text()

    def get_product_price(self, product_name: str) -> str:
        item = self.page.locator(".inventory_item").filter(has_text=product_name)
        return item.locator(".inventory_item_price").inner_text()

    def go_to_cart(self):
        self.page.locator(".shopping_cart_link").click()
