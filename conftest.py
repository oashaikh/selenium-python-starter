"""Top-level fixtures.

Driver creation uses Selenium 4's built-in driver manager (Selenium Manager),
which auto-downloads matching driver binaries. `webdriver-manager` is included
as a fallback for older Selenium installs or air-gapped environments.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Iterator

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pages import HomePage  # noqa: E402

load_dotenv()


def _build_chrome(headed: bool, window: str) -> WebDriver:
    opts = ChromeOptions()
    if not headed:
        opts.add_argument("--headless=new")
    opts.add_argument(f"--window-size={window}")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=opts)


def _build_firefox(headed: bool, window: str) -> WebDriver:
    opts = FirefoxOptions()
    if not headed:
        opts.add_argument("-headless")
    width, height = window.split(",")
    opts.add_argument(f"--width={width}")
    opts.add_argument(f"--height={height}")
    return webdriver.Firefox(options=opts)


def _build_edge(headed: bool, window: str) -> WebDriver:
    opts = EdgeOptions()
    if not headed:
        opts.add_argument("--headless=new")
    opts.add_argument(f"--window-size={window}")
    return webdriver.Edge(options=opts)


_BUILDERS = {"chrome": _build_chrome, "firefox": _build_firefox, "edge": _build_edge}


# --- Fixtures ----------------------------------------------------------------


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ.get("BASE_URL", "https://www.selenium.dev")


@pytest.fixture
def driver() -> Iterator[WebDriver]:
    browser = os.environ.get("BROWSER", "chrome").lower()
    headed = os.environ.get("HEADED", "0") in {"1", "true", "yes"}
    window = os.environ.get("WINDOW_SIZE", "1280,800")
    if browser not in _BUILDERS:
        raise RuntimeError(f"Unknown BROWSER={browser!r}; pick chrome/firefox/edge")

    drv = _BUILDERS[browser](headed, window)
    drv.implicitly_wait(float(os.environ.get("IMPLICIT_WAIT", "5")))
    drv.set_page_load_timeout(float(os.environ.get("PAGE_LOAD_TIMEOUT", "30")))
    try:
        yield drv
    finally:
        drv.quit()


@pytest.fixture
def home_page(driver: WebDriver, base_url: str) -> HomePage:
    return HomePage(driver, base_url)


# --- Failure screenshots ----------------------------------------------------


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if drv:
            Path("test-results").mkdir(exist_ok=True)
            drv.save_screenshot(f"test-results/{item.name}.png")
