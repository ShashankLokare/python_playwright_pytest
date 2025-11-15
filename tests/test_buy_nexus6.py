import time
from app.pages.home_page import HomePage
from app.pages.product_page import ProductPage
from app.pages.cart_page import CartPage


def test_buy_nexus6(page):
    """End-to-end: buy Nexus 6 from demoblaze and verify confirmation."""
    product_name = "Nexus 6"

    home = HomePage(page)
    home.open()

    # click product from home
    home.select_product(product_name)

    product = ProductPage(page)
    # optional assert product page title
    assert product_name in product.title()

    # add to cart (handles dialog)
    product.add_to_cart()

    cart = CartPage(page)
    cart.open()
    cart.place_order()

    # fill with test data
    cart.fill_order_form(
        name="Test User",
        country="Testland",
        city="Testville",
        card="4111111111111111",
        month="12",
        year="2030",
    )
    cart.purchase()

    # verify confirmation
    confirmation_text = cart.get_confirmation_text()
    assert "Thank you for your purchase" in confirmation_text
