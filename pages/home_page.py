"""Example page object: selenium.dev home page."""
from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "/"

    DOWNLOAD_LINK = (By.LINK_TEXT, "Downloads")
    DOCS_LINK = (By.LINK_TEXT, "Documentation")
    HEADLINE = (By.CSS_SELECTOR, "h1")

    def open_downloads(self) -> None:
        self.click(self.DOWNLOAD_LINK)

    def open_docs(self) -> None:
        self.click(self.DOCS_LINK)

    def headline_text(self) -> str:
        return self.visible(self.HEADLINE).text
