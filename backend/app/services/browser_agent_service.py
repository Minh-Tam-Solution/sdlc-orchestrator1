"""
Browser Agent Service - Automated Browser E2E Testing

SDLC Stage: 04 - BUILD
Sprint: 174 - Anthropic Patterns Integration
Framework: SDLC 6.0.5

Purpose:
Lightweight Playwright-based browser agent for automated E2E testing.
Provides async navigation, interaction, and screenshot capabilities
for validating frontend user journeys programmatically.

Architecture:
- Uses Playwright async API for browser automation
- Graceful degradation when Playwright is not installed
- Context manager support for safe resource cleanup
- Global singleton pattern for service reuse

Note:
This is a Sprint 174 prototype. Full browser agent orchestration
(multi-step flows, assertion engine, evidence capture) is planned
for Sprint 176.
"""

import logging
import os
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

try:
    from playwright.async_api import Browser, BrowserContext, Page, async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.info(
        "Playwright not installed. Install with: pip install playwright && playwright install chromium"
    )


class BrowserAgentService:
    """
    Async browser agent for automated E2E testing with Playwright.

    Provides navigation, element interaction, screenshot capture, and
    form filling through a clean async interface with context manager
    support for safe resource lifecycle management.

    Usage:
        async with BrowserAgentService(headless=True) as agent:
            result = await agent.navigate("https://app.example.com/login")
            await agent.fill("input[name='email']", "user@example.com")
            await agent.click("button[type='submit']")
            await agent.screenshot("/tmp/dashboard.png")
    """

    def __init__(
        self,
        headless: bool = True,
        default_timeout_ms: int = 30_000,
    ) -> None:
        """
        Initialize the browser agent configuration.

        Args:
            headless: Run browser in headless mode (no visible window).
            default_timeout_ms: Default timeout for page operations in milliseconds.
        """
        self._headless = headless
        self._default_timeout_ms = default_timeout_ms
        self._playwright: Any = None
        self._browser: Optional["Browser"] = None
        self._context: Optional["BrowserContext"] = None
        self._page: Optional["Page"] = None

    async def _ensure_page(self) -> "Page":
        """
        Lazily initialize Playwright browser, context, and page.

        Returns:
            The active Playwright Page instance.

        Raises:
            RuntimeError: If Playwright is not installed.
        """
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError(
                "Playwright is not installed. "
                "Run: pip install playwright && playwright install chromium"
            )

        if self._page is not None:
            return self._page

        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=self._headless)
        self._context = await self._browser.new_context()
        self._page = await self._context.new_page()
        self._page.set_default_timeout(self._default_timeout_ms)

        logger.info(
            "Browser agent initialized (headless=%s, timeout=%dms)",
            self._headless,
            self._default_timeout_ms,
        )
        return self._page

    async def navigate(self, url: str) -> Dict[str, str]:
        """
        Navigate to a URL and wait for the page to load.

        Args:
            url: The target URL to navigate to.

        Returns:
            Dict with 'title' and 'url' of the loaded page.

        Raises:
            RuntimeError: If Playwright is not installed.
            playwright.async_api.Error: On navigation failure.
        """
        page = await self._ensure_page()
        response = await page.goto(url, wait_until="domcontentloaded")
        title = await page.title()
        current_url = page.url

        status = response.status if response else 0
        logger.info("Navigated to %s (status=%d, title=%r)", current_url, status, title)

        return {"title": title, "url": current_url}

    async def click(self, selector: str) -> Dict[str, str]:
        """
        Click an element identified by a CSS selector.

        Args:
            selector: CSS selector for the target element.

        Returns:
            Dict with 'selector' and 'url' after click.

        Raises:
            RuntimeError: If Playwright is not installed.
            playwright.async_api.Error: If element not found or not clickable.
        """
        page = await self._ensure_page()
        await page.click(selector)
        current_url = page.url

        logger.info("Clicked element '%s' (url=%s)", selector, current_url)
        return {"selector": selector, "url": current_url}

    async def screenshot(self, path: str) -> Dict[str, Any]:
        """
        Capture a full-page screenshot and save to disk.

        Args:
            path: Filesystem path for the PNG screenshot file.

        Returns:
            Dict with 'path' (absolute) and 'size_bytes' of the saved file.

        Raises:
            RuntimeError: If Playwright is not installed.
            OSError: If the path is not writable.
        """
        page = await self._ensure_page()
        await page.screenshot(path=path, full_page=True)

        abs_path = os.path.abspath(path)
        size_bytes = os.path.getsize(abs_path)

        logger.info("Screenshot saved to %s (%d bytes)", abs_path, size_bytes)
        return {"path": abs_path, "size_bytes": size_bytes}

    async def fill(self, selector: str, value: str) -> Dict[str, str]:
        """
        Fill a form field identified by a CSS selector.

        Args:
            selector: CSS selector for the input element.
            value: Text value to fill into the field.

        Returns:
            Dict with 'selector' and 'value' that was filled.

        Raises:
            RuntimeError: If Playwright is not installed.
            playwright.async_api.Error: If element not found or not editable.
        """
        page = await self._ensure_page()
        await page.fill(selector, value)

        logger.info("Filled '%s' with %d characters", selector, len(value))
        return {"selector": selector, "value": value}

    async def get_text(self, selector: str) -> str:
        """
        Get the visible text content of an element.

        Args:
            selector: CSS selector for the target element.

        Returns:
            The text content of the matched element, stripped of
            leading and trailing whitespace.

        Raises:
            RuntimeError: If Playwright is not installed.
            playwright.async_api.Error: If element not found.
        """
        page = await self._ensure_page()
        text = await page.text_content(selector)
        result = (text or "").strip()

        logger.debug("Got text from '%s': %r", selector, result[:100])
        return result

    async def close(self) -> None:
        """
        Close browser and release all Playwright resources.

        Safe to call multiple times; subsequent calls are no-ops.
        """
        if self._page is not None:
            await self._page.close()
            self._page = None

        if self._context is not None:
            await self._context.close()
            self._context = None

        if self._browser is not None:
            await self._browser.close()
            self._browser = None

        if self._playwright is not None:
            await self._playwright.stop()
            self._playwright = None

        logger.info("Browser agent resources released")

    async def __aenter__(self) -> "BrowserAgentService":
        """Enter async context manager."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit async context manager, ensuring resource cleanup."""
        await self.close()


# ---------------------------------------------------------------------------
# Global singleton
# ---------------------------------------------------------------------------

_browser_agent: Optional[BrowserAgentService] = None


def get_browser_agent(
    headless: bool = True,
    default_timeout_ms: int = 30_000,
) -> BrowserAgentService:
    """
    Get or create the global BrowserAgentService singleton.

    Args:
        headless: Run browser in headless mode.
        default_timeout_ms: Default timeout for page operations.

    Returns:
        Shared BrowserAgentService instance.
    """
    global _browser_agent

    if _browser_agent is None:
        _browser_agent = BrowserAgentService(
            headless=headless,
            default_timeout_ms=default_timeout_ms,
        )
        logger.info("Global browser agent created (headless=%s)", headless)

    return _browser_agent
