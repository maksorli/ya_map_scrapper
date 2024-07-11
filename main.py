import itertools
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from seleniumwire import webdriver as wire_webdriver
from selenium.webdriver.common.action_chains import ActionChains
import logging
import sqlite3
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from scrapper.scrapper import PageScrapper
from bs4 import BeautifulSoup
from config import url, proxies

try:
    # Connect to the database or create a new one if it does not exist
    conn = sqlite3.connect("data/ya_maps.db")
    cursor = conn.cursor()

    # Create a table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS organizations
                      (name TEXT, operation_hours TEXT, address TEXT, phone TEXT, link TEXT)"""
    )
    conn.commit()

except sqlite3.Error as e:
    print(f"An error occurred while working with SQLite: {e}")
finally:
    if conn:
        conn.close()

# Configure logger
logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)

# Handlers for logging to file and terminal
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class ProxyRotator:
    """Rotates proxies for each request."""

    def __init__(self, proxies: list):
        self.proxies = itertools.cycle(proxies)
        self.current_proxy = None
        self.request_counter = 0

    def change_proxy(self) -> dict:
        """Switch to the next proxy."""
        self.current_proxy = next(self.proxies)
        self.request_counter = 0
        return self.current_proxy

    def get_proxy(self) -> dict:
        """Get the current proxy, changing it if necessary."""
        if self.request_counter % 2 == 0:
            self.change_proxy()
        self.request_counter += 1
        return self.current_proxy


proxy_rotator = ProxyRotator(proxies)

while True:
    proxy = proxy_rotator.get_proxy()
    logging.info(f"Using proxy: {proxy}")
    prx = {"proxy": proxy}
    with wire_webdriver.Chrome(seleniumwire_options=prx) as driver:
        conn = sqlite3.connect("data/ya_maps.db")
        cursor = conn.cursor()
        driver.get(url)
        actions = ActionChains(driver)
        head_names = driver.find_elements(
            By.CLASS_NAME, "search-business-snippet-view__title"
        )
        head_working_hours = driver.find_elements(
            By.CLASS_NAME, "business-working-status-view"
        )
        head_address = driver.find_elements(
            By.CLASS_NAME, "search-business-snippet-view__address"
        )
        time.sleep(10)  # Ensure the page has loaded

        # Process information
        for name, hours, address in zip(head_names, head_working_hours, head_address):
            print(name.text, hours.text, address.text)
            cursor.execute(
                "INSERT INTO organizations (name, operation_hours, address) VALUES (?,?,?)",
                (name.text, hours.text, address.text),
            )

        conn.commit()

        # Simulate scrolling on the search page
        slider = driver.find_element(By.CSS_SELECTOR, ".scroll__scrollbar-thumb")
        parent_handle = driver.window_handles[0]
        org_id = 0

        try:
            # Main scraping loop
            for i in range(10000):
                ActionChains(driver).click_and_hold(slider).move_by_offset(
                    0, 100
                ).release().perform()
                print("Moved slider by 100 units")

                # Load links every 5 iterations
                if (org_id == 0) or (org_id % 5 == 0):
                    organizations_href = driver.find_elements(
                        By.CLASS_NAME, "search-snippet-view__link-overlay"
                    )

                for organization in organizations_href:
                    print(organization.text)

                # Handle organization tabs
                organization_url = organizations_href[i].get_attribute("href")
                print(organization_url)

                # Open organization tab
                driver.execute_script(f'window.open("{organization_url}","org_tab");')
                child_handle = [x for x in driver.window_handles if x != parent_handle][
                    0
                ]
                driver.switch_to.window(child_handle)
                time.sleep(1)

                soup = BeautifulSoup(driver.page_source, "lxml")
                name = PageScrapper.get_name(soup)
                address = PageScrapper.get_address(soup)
                website = PageScrapper.get_website(soup)
                opening_hours = PageScrapper.get_operation_hours(soup)
                link = driver.current_url

                driver.close()
                driver.switch_to.window(parent_handle)
                time.sleep(1)
        except Exception as e:
            logger.error(f"Error during operation: {e}")

        driver.quit()

    time.sleep(3)  # Wait before next proxy rotation
