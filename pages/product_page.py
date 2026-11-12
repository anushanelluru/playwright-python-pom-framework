import logging
from playwright.sync_api import Page, expect
from base.base_page import BasePage

logger = logging.getLogger(__name__)


class ProductPage(BasePage):
    """
    Playwright Page Object representing the Product Details page.
    Validates product specifications, title display, and cart addition.
    """

    # Selectors
    PRODUCT_TITLE = "#productTitle"
    ADD_TO_CART_BUTTON = "#add-to-cart-button"
    PRICE_DISPLAY = "#corePriceDisplay_desktop_feature_div .a-price .a-offscreen, #priceblock_ourprice"
    CART_SUCCESS_BANNER = "#NATC_SMART_WAGON_CONF_MSG_SUCCESS, #sw-atc-confirmation, h1.a-size-medium-plus"

    def __init__(self, page: Page):
        super().__init__(page)

    def is_loaded(self) -> bool:
        """Verifies if the Product Details page title is visible."""
        return self.is_element_visible(self.PRODUCT_TITLE, timeout=12000)

    def get_product_title(self) -> str:
        """Retrieves and returns the full product headline title."""
        self.wait_for_element_visible(self.PRODUCT_TITLE)
        title_locator = self.get_locator(self.PRODUCT_TITLE).first
        return title_locator.inner_text().strip()

    def is_add_to_cart_available(self) -> bool:
        """Checks if the Add to Cart button is present."""
        return self.is_element_visible(self.ADD_TO_CART_BUTTON, timeout=5000)

    def add_to_cart(self):
        """Clicks the Add to Cart button."""
        logger.info("Clicking 'Add to Cart'...")
        self.click_element(self.ADD_TO_CART_BUTTON)

    def is_added_to_cart_confirmed(self) -> bool:
        """Verifies if cart addition confirmation message appears."""
        return self.is_element_visible(self.CART_SUCCESS_BANNER, timeout=8000)
