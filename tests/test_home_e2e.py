"""Browser-driven smoke tests against selenium.dev."""
from __future__ import annotations

import pytest

from pages import HomePage


@pytest.mark.smoke
def test_home_loads(home_page: HomePage) -> None:
    home_page.open()
    assert "Selenium" in home_page.driver.title


@pytest.mark.regression
def test_open_docs_navigates(home_page: HomePage) -> None:
    home_page.open()
    home_page.open_docs()
    assert "documentation" in home_page.driver.current_url.lower()
