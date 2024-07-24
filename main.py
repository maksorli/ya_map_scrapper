import time
import os
import subprocess
from selenium.webdriver.common.by import By
from selenium import webdriver
from seleniumwire import webdriver as wire_webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from config import url, proxies
from scrapper.proxy_rotator import ProxyRotator
from data.database_manager import DatabaseManager
from logging_path.logger_module import LoggerSetup
from models.scroller import Scroller


def main() -> None:
    """
    Main function to execute the web scraping and database insertion.
    """
    database = DatabaseManager("data/ya_maps.db")

    logger_setup = LoggerSetup("MyLogger")
    logger = logger_setup.logger

    response = input("Please enter link with found places: ")
    url = response.lower()

    proxy_rotator = ProxyRotator(proxies)
    link_collect = False

    while True and not link_collect:
        proxy = proxy_rotator.get_proxy()
        logger.info(f"Using proxy: {proxy}")
        prx = {"proxy": proxy}

        with wire_webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            seleniumwire_options=prx,
        ) as driver:
            driver.set_window_size(1200, 900)
            driver.get(url)
            time.sleep(1)
            actions = ActionChains(driver)
            scroller = Scroller(driver)
            end_of_scroll = False

            try:
                while not end_of_scroll:
                    end_of_scroll = scroller.scroll_element(
                        ".scroll__scrollbar-thumb", 0, 100
                    )

                # Collect links
                organizations_href = driver.find_elements(
                    By.CLASS_NAME, "search-snippet-view__link-overlay"
                )
                logger.info(f"Count of collected links: {len(organizations_href)}")

                database.connect()
                for href in organizations_href:
                    link = href.get_attribute("href")
                    name = href.text
                    database.insert_organization(name=name, link=link)
                    link_collect = True
                driver.quit()

            except Exception as e:
                print(f"An error occurred: {e}")

            finally:
                driver.quit()

    response = input("Do you want to collect info from link (Y/N): ").strip().lower()

    if response == "y":
        run_another_script("link_scrap.py")


def run_another_script(script_name: str) -> None:
    """
    Run another Python script from the same directory.

    Args:
        script_name (str): The name of the script to run.
    """
    script_path = os.path.join(os.path.dirname(__file__), script_name)

    try:
        subprocess.run(["python", script_path], check=True)
    except Exception as e:
        print(f"An error occurred while running the script: {e}")


if __name__ == "__main__":
    main()
