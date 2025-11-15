from .base_page import BasePage
from .locators import Locators


class HomePage(BasePage):
    def open(self):
        self.goto("")

    def select_product(self, product_name: str):
        # uses a text locator to find product link by name
        locator = Locators.PRODUCT_LINK_BY_NAME.format(name=product_name)
        # ensure product is visible and click
        self.page.locator(locator).first.wait_for(state="visible", timeout=5000)
        self.page.click(locator)
