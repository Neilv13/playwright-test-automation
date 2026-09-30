# Playwright Test Automation Framework

A UI test automation framework built with Playwright (Python) and the Page Object Model, covering real end-to-end user flows on [SauceDemo](https://www.saucedemo.com/), with a CI pipeline designed around test-suite speed, not just correctness.

## Architecture

Built with the **Page Object Model (POM)** pattern - each page's locators and actions are encapsulated in a dedicated class (`pages/login_page.py`, `pages/inventory_page.py`), so tests read as plain orchestration of user actions rather than raw locator manipulation:

```python
def test_add_to_cart(page: Page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(page)
    inventory_page.add_to_cart("Sauce Labs Backpack")

    expect(inventory_page.cart_badge).to_have_text("1")
```

If a locator ever changes on the real site, it's fixed in exactly one place - the relevant page object - not scattered across every test that touches that page.

## Tests covered

- Login (`tests/test_login.py`)
- Add to cart (`tests/test_add_to_cart.py`)
- Remove from cart, get product price, navigate to cart - supporting page-object methods for further test coverage

## CI design: staged by speed, not cost

Unlike an LLM-evaluation pipeline (where staging is about avoiding unnecessary API cost), a growing UI test suite's real constraint is **speed and stability** - running every test on every commit doesn't scale. This pipeline reflects that with two separate jobs:

- **Smoke test** - runs the single most critical flow (login) on every push and pull request. Fast feedback on the one thing that has to work for anything else to be testable.
- **Full regression suite** - runs the entire test suite on a nightly schedule (and on manual trigger), not on every commit. Catches regressions across all covered flows without slowing down every single push.

## Running locally

```bash
pip install -r requirements.txt
playwright install chromium
pytest tests/ -v                    # full suite
pytest tests/test_login.py -v       # smoke test only
pytest tests/ -v --headed           # watch the browser run
pytest tests/ -v --headed --slowmo 1000   # watch it run slowly, step by step
```

## Tech stack

Python, Playwright, pytest, Page Object Model, GitHub Actions.
