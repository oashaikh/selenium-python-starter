"""Network-free unit tests of page-object logic.

These don't launch a browser — they verify the URL building and locator
construction with a mocked WebDriver. Useful as fast smoke checks.
"""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from pages import HomePage


@pytest.mark.headless
@pytest.mark.smoke
def test_open_uses_base_url_plus_path() -> None:
    driver = MagicMock()
    page = HomePage(driver, "https://example.com/")
    page.open("/about")
    driver.get.assert_called_once_with("https://example.com/about")


@pytest.mark.headless
@pytest.mark.smoke
def test_open_uses_class_url_when_no_path() -> None:
    driver = MagicMock()
    page = HomePage(driver, "https://example.com")
    page.open()
    driver.get.assert_called_once_with("https://example.com/")


@pytest.mark.headless
def test_base_url_trailing_slash_normalised() -> None:
    driver = MagicMock()
    page = HomePage(driver, "https://example.com//")
    assert page.base_url == "https://example.com"


@pytest.mark.headless
def test_path_without_leading_slash() -> None:
    driver = MagicMock()
    page = HomePage(driver, "https://example.com")
    page.open("about")
    driver.get.assert_called_once_with("https://example.com/about")
