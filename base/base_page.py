import logging
from typing import List
from playwright.sync_api import Page, Locator, expect
from utils.config_reader import ConfigReader

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class BasePage:
    """
    BasePage encapsulates common Playwright browser interactions.
    Leverages Playwright's native auto-waiting mechanisms (visibility, stability, and editability)
    while providing custom logging and fallback behaviors.
    """

    def __init__(self, page: Page):
        self.page = page
        self.default_timeout = ConfigReader.get_timeout()
        self.page.set_default_timeout(self.default_timeout)

    def navigate_to(self, url: str):
        """Navigates to a given URL with domcontentloaded wait state."""
        logger.info(f"Navigating to URL: {url}")
        self.page.goto(url, wait_until="domcontentloaded", timeout=self.default_timeout)

    def get_locator(self, selector: str) -> Locator:
        """Returns a Playwright Locator for the given CSS/XPath selector."""
        return self.page.locator(selector)

    def wait_for_element_visible(self, selector: str, timeout: int = None) -> Locator:
        """Explicitly asserts that an element becomes visible within the timeout."""
        locator = self.get_locator(selector)
        logger.debug(f"Waiting for visibility of: {selector}")
        expect(locator.first).to_be_visible(timeout=timeout or self.default_timeout)
        return locator

    def click_element(self, selector: str, timeout: int = None):
        """Performs an auto-waiting safe click on the element."""
        logger.info(f"Clicking element: {selector}")
        self.page.click(selector, timeout=timeout or self.default_timeout)

    def enter_text(self, selector: str, text: str, timeout: int = None):
        """Fills input text into the target element with auto-clear."""
        logger.info(f"Typing '{text}' into: {selector}")
        self.page.fill(selector, text, timeout=timeout or self.default_timeout)

    def get_element_text(self, selector: str, timeout: int = None) -> str:
        """Extracts and strips inner text from the first matched element."""
        locator = self.get_locator(selector).first
        self.wait_for_element_visible(selector, timeout)
        text = locator.inner_text(timeout=timeout or self.default_timeout)
        return text.strip()

    def is_element_visible(self, selector: str, timeout: int = 3000) -> bool:
        """Checks if an element is currently visible within a short timeout without throwing."""
        try:
            return self.page.locator(selector).first.is_visible(timeout=timeout)
        except Exception:
            return False

    def scroll_to_element(self, selector: str):
        """Scrolls the target element into the viewport."""
        self.page.locator(selector).first.scroll_into_view_if_needed()

    def take_screenshot(self, file_path: str, full_page: bool = False):
        """Captures a screenshot of the current page."""
        logger.info(f"Saving screenshot to: {file_path}")
        self.page.screenshot(path=file_path, full_page=full_page)

    def get_page_title(self) -> str:
        """Returns the document title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Returns the current page URL."""
        return self.page.url
