# Maps each agent-generated test case (by tc_id) to the real Playwright test
# that automates it. A tc_id with no entry here is a test the agent designed
# but that has no real automation behind it yet - that gap is exactly what
# the coverage report below is for.

AUTOMATION_MAP = {
    "TC_LOG_001": "tests/test_login.py::test_login",
    "TC_LOG_002": "tests/test_invalid_login.py::test_invalid_login",
    "TC_CART_001": "tests/test_add_to_cart.py::test_add_to_cart",
    "TC_CART_002": "tests/test_multiple_products.py::test_multiple_products",
    "TC_LOG_003": "tests/test_empty_login.py::test_empty_login",
}
