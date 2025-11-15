import allure
from app.pages.home_page import HomePage
from app.pages.product_page import ProductPage
from app.pages.cart_page import CartPage


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
        allure.attach.file(
            page.screenshot(),
            name="homepage",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step(f"Search and select '{product_name}' product"):
        home.select_product(product_name)
        allure.attach.file(
            page.screenshot(),
            name="product_selected",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Verify product page loaded"):
        product = ProductPage(page)
        title = product.title()
        assert product_name in title, f"Product title should contain '{product_name}', got '{title}'"
        allure.attach.file(
            page.screenshot(),
            name="product_page",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Add product to cart"):
        product.add_to_cart()
        allure.attach.file(
            page.screenshot(),
            name="added_to_cart",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Open shopping cart"):
        cart = CartPage(page)
        cart.open()
        allure.attach.file(
            page.screenshot(),
            name="cart_page",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Click place order"):
        cart.place_order()
        allure.attach.file(
            page.screenshot(),
            name="place_order_modal",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Fill order form with test data"):
        cart.fill_order_form(
            name="Test User",
            country="Testland",
            city="Testville",
            card="4111111111111111",
            month="12",
            year="2030",
        )
        allure.attach.file(
            page.screenshot(),
            name="form_filled",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Complete purchase"):
        cart.purchase()
        allure.attach.file(
            page.screenshot(),
            name="purchase_confirmation",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Verify purchase confirmation"):
        confirmation_text = cart.get_confirmation_text()
        assert "Thank you for your purchase" in confirmation_text, \
            f"Expected confirmation message, got: {confirmation_text}"
        allure.attach(
            f"Confirmation: {confirmation_text}",
            name="confirmation_message",
            attachment_type=allure.attachment_type.TEXT,
        )
