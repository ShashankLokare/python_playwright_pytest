import allure
import tempfile
import os
from app.pages.home_page import HomePage
from app.pages.product_page import ProductPage
from app.pages.cart_page import CartPage


def _save_screenshot(page, name: str):
    """Helper to save screenshot and attach to Allure."""
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            temp_path = f.name
        page.screenshot(path=temp_path)
        allure.attach.file(
            temp_path,
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
        os.unlink(temp_path)
    except Exception as e:
        print(f"Error capturing screenshot '{name}': {e}")


@allure.feature("Shopping")
@allure.story("Purchase Product")
@allure.title("Buy Nexus 6 from DemoBlaze")
@allure.severity(allure.severity_level.CRITICAL)
def test_buy_nexus6(page):
    """End-to-end: buy Nexus 6 from demoblaze and verify confirmation."""
    product_name = "Nexus 6"

    with allure.step("Open homepage"):
        home = HomePage(page)
        home.open()
        _save_screenshot(page, "homepage")

    with allure.step(f"Search and select '{product_name}' product"):
        home.select_product(product_name)
        _save_screenshot(page, "product_selected")

    with allure.step("Verify product page loaded"):
        product = ProductPage(page)
        title = product.title()
        assert product_name in title, f"Product title should contain '{product_name}', got '{title}'"
        _save_screenshot(page, "product_page")

    with allure.step("Add product to cart"):
        product.add_to_cart()
        _save_screenshot(page, "added_to_cart")

    with allure.step("Open shopping cart"):
        cart = CartPage(page)
        cart.open()
        _save_screenshot(page, "cart_page")

    with allure.step("Click place order"):
        cart.place_order()
        _save_screenshot(page, "place_order_modal")

    with allure.step("Fill order form with test data"):
        cart.fill_order_form(
            name="Test User",
            country="Testland",
            city="Testville",
            card="4111111111111111",
            month="12",
            year="2030",
        )
        _save_screenshot(page, "form_filled")

    with allure.step("Complete purchase"):
        cart.purchase()
        _save_screenshot(page, "purchase_confirmation")

    with allure.step("Verify purchase confirmation"):
        confirmation_text = cart.get_confirmation_text()
        assert "Thank you for your purchase" in confirmation_text, \
            f"Expected confirmation message, got: {confirmation_text}"
        allure.attach(
            f"Confirmation: {confirmation_text}",
            name="confirmation_message",
            attachment_type=allure.attachment_type.TEXT,
        )
