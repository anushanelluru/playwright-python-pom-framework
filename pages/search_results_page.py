import logging
from playwright.sync_api import Page, expect
from base.base_page import BasePage

logger = logging.getLogger(__name__)


class SearchResultsPage(BasePage):
    """
    Playwright Page Object for the Amazon Search Results page.
    Encapsulates results counting, validation, and product selection.
    """

    # Selectors
    SEARCH_RESULT_CARDS = "div[data-component-type='s-search-result']"
    PRODUCT_TITLE_LINKS = "div[data-component-type='s-search-result'] h2 a, [data-cy='title-recipe'] h2 a"
    RESULTS_INFO_BAR = "span[data-component-type='s-result-info-bar'], h1.a-size-base"

    def __init__(self, page: Page):
        super().__init__(page)

    def is_loaded(self) -> bool:
        """Verifies that search result cards are displayed."""
        return self.is_element_visible(self.SEARCH_RESULT_CARDS, timeout=10000)

    def get_search_results_count(self) -> int:
        """Counts the total visible product cards on the current page."""
        self.wait_for_element_visible(self.SEARCH_RESULT_CARDS)
        cards = self.get_locator(self.SEARCH_RESULT_CARDS)
        count = cards.count()
        logger.info(f"Detected {count} product cards on search results page.")
        return count

    def get_first_product_title(self) -> str:
        """Retrieves the title of the first search result."""
        first_title = self.get_locator(self.PRODUCT_TITLE_LINKS).first
        expect(first_title).to_be_visible(timeout=self.default_timeout)
        return first_title.inner_text().strip()

    def select_first_product(self):
        """
        Clicks the first product card link.
        Gracefully handles both same-tab navigation and target='_blank' new tab openings in Playwright.
        """
        from pages.product_page import ProductPage

        first_link = self.get_locator(self.PRODUCT_TITLE_LINKS).first
        expect(first_link).to_be_visible(timeout=self.default_timeout)

        target_attr = first_link.get_attribute("target")
        logger.info(f"Clicking first product (target='{target_attr}')...")

        if target_attr == "_blank":
            # Amazon opens link in a new browser tab/page
            with self.page.context.expect_page() as new_page_info:
                first_link.click()
            new_page = new_page_info.value
            new_page.wait_for_load_state("domcontentloaded")
            return ProductPage(new_page)
        else:
            first_link.click()
            self.page.wait_for_load_state("domcontentloaded")
            return ProductPage(self.page)
