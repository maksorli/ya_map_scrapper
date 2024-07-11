from bs4 import BeautifulSoup
from selenium.common.exceptions import (
    NoSuchElementException,
    MoveTargetOutOfBoundsException,
)
from selenium.webdriver import ActionChains


class PageScrapper(object):
    """Class for parsing data from a BeautifulSoup object."""

    @staticmethod
    def get_name(soup_content: BeautifulSoup) -> str:
        """Retrieve the name of the organization."""
        try:
            name = ""
            for data in soup_content.find_all(
                "h1", {"class": "orgpage-header-view__header"}
            ):
                name = data.getText()
            return name
        except Exception:
            return ""

    @staticmethod
    def get_address(soup_content: BeautifulSoup) -> str:
        """Retrieve the address of the organization."""
        try:
            address = ""
            for data in soup_content.find_all(
                "a", {"class": "business-contacts-view__address-link"}
            ):
                address = data.getText()
            return address
        except Exception:
            return ""

    @staticmethod
    def get_website(soup_content: BeautifulSoup) -> str:
        """Retrieve the website of the organization."""
        try:
            website = ""
            for data in soup_content.find_all(
                "span", {"class": "business-urls-view__text"}
            ):
                website = data.getText()
            return website
        except Exception:
            return ""

    @staticmethod
    def get_operation_hours(soup_content: BeautifulSoup) -> list:
        """Retrieve the opening hours of the organization."""
        opening_hours = []
        try:
            for data in soup_content.find_all("meta", {"itemprop": "openingHours"}):
                opening_hours.append(data.get("content"))
            return opening_hours
        except Exception:
            return []
