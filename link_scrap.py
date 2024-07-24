import requests
import aiohttp
import asyncio
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from scrapper.scrapper import PageScrapper
from data.database_manager import DatabaseManager
from config import proxies_aiohttp_socks, headers
from logging_path.logger_module import LoggerSetup
from itertools import cycle


def main() -> None:
    """
    Main function to execute the scraping and database update.
    """
    logger_setup = LoggerSetup("MyLogger")
    logger = logger_setup.logger
    database = DatabaseManager("data/ya_maps.db")

    # Create UserAgent object
    ua = UserAgent()

    # Generate random User-Agent
    user_agent = ua.random
    print(f"Using User-Agent: {user_agent}")

    headers = {"User-Agent": user_agent}

    # Connect to the database and fetch all links
    db_manager = DatabaseManager("data/ya_maps.db")
    db_manager.connect()
    links = db_manager.fetch_all_links()
    db_manager.close()

    # Cycle through proxies
    proxy_cycle = cycle(proxies_aiohttp_socks)

    for link in links:
        proxy = next(proxy_cycle)

        response = requests.get(
            link, headers=headers, proxies={"http": proxy, "https": proxy}
        )
        logger.info(f"{proxy}: {response.status_code}")

        soup = BeautifulSoup(response.text, "lxml")
        name = PageScrapper.get_name(soup)
        address = PageScrapper.get_address(soup)
        website = PageScrapper.get_website(soup)
        opening_hours = PageScrapper.get_operation_hours(soup)
        contacts = PageScrapper.get_contacts(soup)

        database.connect()
        database.insert_organization(
            key=link,
            address=address,
            website=website,
            operation_hours=opening_hours,
            contacts=contacts,
        )
        database.close()

        time.sleep(1)
        print(f"Data f: {name}, {address}, {website}, {contacts}, {opening_hours}")

    # Prompt the user to run another script
    response = (
        input("Do you want to run another script from this folder? (yes/no): ")
        .strip()
        .lower()
    )
    if response == "yes":
        run_another_script("other_script.py")


def run_another_script(script_name: str) -> None:
    """
    Run another Python script from the same directory.

    Args:
        script_name (str): The name of the script to run.
    """
    import os
    import subprocess

    script_path = os.path.join(os.path.dirname(__file__), script_name)
    try:
        subprocess.run(["python", script_path], check=True)
    except Exception as e:
        print(f"An error occurred while running the script: {e}")


if __name__ == "__main__":
    main()
