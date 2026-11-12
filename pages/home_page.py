import logging
from playwright.sync_api import Page, expect
from base.base_page import BasePage
from pages.search_results_page import SearchResultsPage

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """
    Playwright Page Object representing the Amazon Home Page.
    Handles product search and initial navigation.
    """

    # CSS / XPath Selectors
    SEARCH_INPUT = "#twotabsearchtextbox"
    SEARCH_BUTTON = "#nav-search-submit-button"
    NAV_LOGO = "#nav-logo-sprites"
    DISMISS_LOCATION_BUTTON = "input[data-action-type='DISMISS']"

    def __init__(self, page: Page):
        super().__init__(page)

    def load(self, url: str):
        """Navigates to the Amazon home page and handles optional location popups."""
        self.navigate_to(url)
        self.dismiss_location_popup_if_present()

    def dismiss_location_popup_if_present(self):
        """Dismisses the delivery location prompt if displayed."""
        try:
            if self.is_element_visible(self.DISMISS_LOCATION_BUTTON, timeout=2000):
                self.click_element(self.DISMISS_LOCATION_BUTTON, timeout=2000)
                logger.info("Dismissed delivery location prompt.")
        except Exception:
            pass

    def is_loaded(self) -> bool:
        """Verifies if the Home page search bar is rendered and visible."""
        return self.is_element_visible(self.SEARCH_INPUT, timeout=5000)

    def enter_search_query(self, query: str):
        """Enters search keywords into the search box."""
        self.enter_text(self.SEARCH_INPUT, query)

    def click_search_button(self) -> SearchResultsPage:
        """Clicks search button and returns the SearchResultsPage."""
        self.click_element(self.SEARCH_BUTTON)
        self.page.wait_for_load_state("domcontentloaded")
        return SearchResultsPage(self.page)

    def search_for_product(self, query: str) -> SearchResultsPage:
        """Combined action: type query and submit."""
        self.enter_search_query(query)
        return self.click_search_button()
