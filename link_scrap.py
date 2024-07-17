import requests

from config import headers
import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from aiohttp_socks import ChainProxyConnector
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent
from scrapper.scrapper import PageScrapper
from data.database_manager import DatabaseManager
from config import  proxies_aiohttp_socks
from logging_path.logger_module import  LoggerSetup
from config import headers
from itertools import cycle
logger_setup = LoggerSetup("MyLogger")
logger = logger_setup.logger

db_manager = DatabaseManager('data/ya_maps.db')
db_manager.connect()
links = db_manager.fetch_all_links()
db_manager.close()

proxy_cycle = cycle(proxies_aiohttp_socks)   

for link in links:
    proxy = next(proxy_cycle)   
    try:
        response = requests.get(link, headers=headers, proxies={"http": proxy, "https": proxy})
        logger.info(response.status_code)   
        soup = BeautifulSoup(response.text, 'lxml')
        name = PageScrapper.get_name(soup)
        address = PageScrapper.get_address(soup)
        website = PageScrapper.get_website(soup)
        opening_hours = PageScrapper.get_operation_hours(soup)
        contacts = PageScrapper.get_contacts(soup)
        logger.info(f"Data from {link} : {name}, {address}, {website}, {contacts}, {opening_hours}")
    except requests.RequestException as e:
        logger.info(f"Failed to fetch {link}: {str(e)}")