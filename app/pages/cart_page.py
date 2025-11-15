from .base_page import BasePage
from .locators import Locators


class CartPage(BasePage):
    def open(self):
        self.goto("")
        # navigate to cart via top link
        self.page.click(Locators.CART_LINK)

    def place_order(self):
        self.page.click(Locators.PLACE_ORDER_BUTTON)
        # wait for modal fields
        self.page.locator(Locators.ORDER_NAME).wait_for(state="visible", timeout=5000)

    def fill_order_form(self, name: str, country: str, city: str, card: str, month: str, year: str):
        self.page.fill(Locators.ORDER_NAME, name)
        self.page.fill(Locators.ORDER_COUNTRY, country)
        self.page.fill(Locators.ORDER_CITY, city)
        self.page.fill(Locators.ORDER_CARD, card)
        self.page.fill(Locators.ORDER_MONTH, month)
        self.page.fill(Locators.ORDER_YEAR, year)

    def purchase(self):
        self.page.click(Locators.PURCHASE_BUTTON)
        # wait for confirmation modal
        self.page.locator(Locators.CONFIRMATION_MODAL).wait_for(state="visible", timeout=10000)

    def get_confirmation_text(self) -> str:
        return self.page.locator(Locators.CONFIRM_TEXT).inner_text().strip()
