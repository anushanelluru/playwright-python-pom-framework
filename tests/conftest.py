import os
import pytest
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page
from utils.config_reader import ConfigReader


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Customizes the Playwright Browser Context across all test sessions.
    Configures standard desktop viewport, custom user-agent, and permissions.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
        "ignore_https_errors": True,
        "locale": "en-US",
    }


@pytest.fixture(scope="function", autouse=True)
def configure_page_timeouts(page: Page):
    """Sets standard timeouts and window dimensions for each test page."""
    timeout_ms = ConfigReader.get_timeout()
    page.set_default_timeout(timeout_ms)
    page.set_default_navigation_timeout(timeout_ms)
    yield page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    PyTest hook that captures a full-page Playwright screenshot automatically
    upon any test failure and attaches it to the pytest-html report.
    """
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        # Check if 'page' fixture exists in the test function arguments
        page: Page = item.funcargs.get("page", None)
        if page:
            project_root = Path(__file__).resolve().parent.parent
            screenshot_dir = project_root / "reports" / "screenshots"
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_file = screenshot_dir / f"{item.name}_{timestamp}.png"

            try:
                page.screenshot(path=str(screenshot_file), full_page=True)
                try:
                    import pytest_html
                    extras.append(pytest_html.extras.image(str(screenshot_file)))
                except ImportError:
                    pass
            except Exception as e:
                print(f"Warning: Could not capture Playwright screenshot on failure: {e}")

        report.extras = extras
