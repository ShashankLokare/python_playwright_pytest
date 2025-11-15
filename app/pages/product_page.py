from .base_page import BasePage
from .locators import Locators


class ProductPage(BasePage):
    def add_to_cart(self):
        # Accept the alert that appears after adding to cart
        # Use event handler style for dialog to support different Playwright bindings
        def _on_dialog(dialog):
            try:
                dialog.accept()
            except Exception:
                pass

        self.page.once("dialog", _on_dialog)
        self.page.click(Locators.ADD_TO_CART_BUTTON)

    def title(self) -> str:
        return self.page.locator(Locators.PRODUCT_TITLE).inner_text().strip()
