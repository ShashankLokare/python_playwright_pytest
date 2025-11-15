from enum import Enum


class Locators:
    """Centralized selectors used by page objects."""

    # Top navigation
    CART_LINK = "#cartur"

    # Home / product list
    # Use a link selector to target product anchors by visible text.
    PRODUCT_LINK_BY_NAME = "a:has-text('{name}')"

    # Product page
    ADD_TO_CART_BUTTON = "a:has-text('Add to cart')"
    PRODUCT_TITLE = "h2.name"

    # Cart page
    PLACE_ORDER_BUTTON = "button[data-target='#orderModal']"
    PURCHASE_BUTTON = "button[onclick='purchaseOrder()']"

    # Order modal fields
    ORDER_NAME = "#name"
    ORDER_COUNTRY = "#country"
    ORDER_CITY = "#city"
    ORDER_CARD = "#card"
    ORDER_MONTH = "#month"
    ORDER_YEAR = "#year"

    # Purchase confirmation
    CONFIRMATION_MODAL = ".sweet-alert"
    CONFIRM_TEXT = ".sweet-alert h2"
