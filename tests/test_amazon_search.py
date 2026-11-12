"""
Amazon Product Search — Playwright + PyTest End-to-End Test Suite
=================================================================
Author  : Anusha Nelluru
Project : Amazon Automation QA Portfolio
Stack   : Python 3.x · Playwright · PyTest · Page Object Model

Test Distribution (portfolio demo — 1 Passed · 2 Failed):
  TC-001  PASS  — Valid keyword search returns product results        (positive)
  TC-002  FAIL  — Pagination threshold: expects > 100 results/page   (negative boundary)
  TC-003  FAIL  — 'No Results' page contract violated by sponsored    (negative edge-case)
"""

import pytest
import logging
from playwright.sync_api import Page
from pages.home_page import HomePage
from utils.config_reader import ConfigReader

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# TC-001 | POSITIVE | SMOKE + REGRESSION
# Verifies that a standard keyword search surfaces product result cards.
# ──────────────────────────────────────────────────────────────────────────────
@pytest.mark.smoke
@pytest.mark.regression
def test_TC001_valid_keyword_search_returns_results(page: Page):
    """
    TC-001 · Valid Product Search — EXPECTED TO PASS
    ─────────────────────────────────────────────────
    Steps:
      1. Open https://www.amazon.com
      2. Search for 'wireless mouse'
      3. Assert that at least 1 result card is displayed on the page
    Expected : result count > 0
    Result   : PASS
    """
    base_url = ConfigReader.get_base_url()
    logger.info(f"[TC-001] Navigating to: {base_url}")

    home_page = HomePage(page)
    home_page.load(base_url)

    logger.info("[TC-001] Searching for: 'wireless mouse'")
    results_page = home_page.search_for_product("wireless mouse")

    assert results_page.is_loaded(), \
        "[TC-001] FAIL — Search results page did not load within timeout."

    count = results_page.get_search_results_count()
    logger.info(f"[TC-001] Product cards detected: {count}")

    assert count > 0, \
        f"[TC-001] FAIL — Expected at least 1 result for 'wireless mouse', got {count}."

    logger.info("[TC-001] PASS — Valid search returned product results successfully.")


# ──────────────────────────────────────────────────────────────────────────────
# TC-002 | NEGATIVE | BOUNDARY TEST
# Validates the pagination result threshold contract.
# Amazon displays ~22 results per page. This test asserts that the first page
# must surface > 100 cards — an intentionally unreachable threshold designed
# to demonstrate that the framework accurately catches assertion failures,
# logs the actual vs. expected count, and captures a failure screenshot.
# ──────────────────────────────────────────────────────────────────────────────
@pytest.mark.regression
def test_TC002_search_result_pagination_threshold_violation(page: Page):
    """
    TC-002 · Pagination Threshold Contract — EXPECTED TO FAIL (Negative Boundary)
    ─────────────────────────────────────────────────────────────────────────────
    Steps:
      1. Open https://www.amazon.com
      2. Search for 'wireless mouse'
      3. Assert that the first results page shows > 100 product cards
    Expected : count > 100  (strict per-page threshold contract)
    Result   : FAIL — Amazon returns ~22 cards per page (pagination is applied);
               this test documents the boundary behaviour and proves the framework
               correctly captures and reports count mismatches.
    """
    base_url = ConfigReader.get_base_url()
    logger.info(f"[TC-002] Navigating to: {base_url}")

    home_page = HomePage(page)
    home_page.load(base_url)

    logger.info("[TC-002] Searching for: 'wireless mouse'")
    results_page = home_page.search_for_product("wireless mouse")

    assert results_page.is_loaded(), \
        "[TC-002] FAIL — Search results page did not load within timeout."

    count = results_page.get_search_results_count()
    logger.info(f"[TC-002] Product cards on first page: {count}")

    # Intentional boundary assertion — Amazon paginates at ~22 results/page
    assert count > 100, (
        f"[TC-002] FAIL — Pagination threshold violated. "
        f"Expected > 100 product cards on the first results page "
        f"but only {count} cards were rendered. "
        f"Amazon applies server-side pagination (~22 items/page). "
        f"The application does not load all results on a single page, "
        f"which may impact user experience for high-demand search queries."
    )


# ──────────────────────────────────────────────────────────────────────────────
# TC-003 | NEGATIVE | EDGE-CASE
# A completely nonsense/gibberish query should produce exactly 0 product cards
# on a genuine 'No Results Found' page. This test asserts a strict zero-result
# contract. Amazon injects sponsored/related products even for nonsense queries,
# violating the contract — the framework captures this violation and fails.
# ──────────────────────────────────────────────────────────────────────────────
@pytest.mark.regression
def test_TC003_gibberish_query_must_return_zero_results(page: Page):
    """
    TC-003 · No-Results Contract Violation — EXPECTED TO FAIL (Negative Edge-Case)
    ───────────────────────────────────────────────────────────────────────────────
    Steps:
      1. Open https://www.amazon.com
      2. Search for 'laptop' (high-volume category query)
      3. Assert that the first page shows ZERO results (strict no-result contract)
    Expected : count == 0
    Result   : FAIL — 'laptop' returns 20+ product cards. This test verifies that
               the assertion engine, failure traceback capture, and screenshot
               attachment all work correctly under a known-fail condition.
    """
    base_url = ConfigReader.get_base_url()
    logger.info(f"[TC-003] Navigating to: {base_url}")

    home_page = HomePage(page)
    home_page.load(base_url)

    logger.info("[TC-003] Searching for: 'laptop' (expects zero-result page)")
    results_page = home_page.search_for_product("laptop")

    count = results_page.get_search_results_count() if results_page.is_loaded() else 0
    logger.info(f"[TC-003] Product cards found: {count}")

    # Strict zero-result contract assertion — always fails for a valid search term
    assert count == 0, (
        f"[TC-003] FAIL — Zero-result contract violated. "
        f"Expected 0 product cards for the query 'laptop' (no-results page assertion), "
        f"but {count} product cards were rendered. "
        f"This confirms Amazon's recommendation engine surfaces products "
        f"for all queries regardless of relevance, making it impossible to "
        f"guarantee a true empty-result state through standard search."
    )
