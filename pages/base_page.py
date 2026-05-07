"""Shared base class for page objects."""
from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    URL: str = "/"
    DEFAULT_TIMEOUT: float = 10.0

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    def open(self, path: str | None = None) -> None:
        target = path or self.URL
        self.driver.get(f"{self.base_url}{target if target.startswith('/') else '/' + target}")

    def wait(self, timeout: float | None = None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT)

    def find(self, locator: tuple[str, str], timeout: float | None = None) -> WebElement:
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator: tuple[str, str], timeout: float | None = None) -> None:
        self.wait(timeout).until(EC.element_to_be_clickable(locator)).click()

    def visible(self, locator: tuple[str, str], timeout: float | None = None) -> WebElement:
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def screenshot(self, name: str) -> str:
        path = f"test-results/{name}.png"
        self.driver.save_screenshot(path)
        return path
