import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from seleniumwire import webdriver as wire_webdriver
from selenium.webdriver.common.action_chains import ActionChains
import logging
from bs4 import BeautifulSoup
from config import url, proxies
from selenium.webdriver.support import expected_conditions as EC
from data.database_manager import DatabaseManager
from models.scroller import Scroller
from logging.logger import  LoggerSetup
database = DatabaseManager('data/ya_maps.db')
 

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

def get_visible_content(driver):
    # Получаем весь видимый текст на странице
    return driver.find_element(By.TAG_NAME, "body").text
 


with wire_webdriver.Chrome(seleniumwire_options=proxies[1]) as driver:
    driver.get(url)
    time.sleep(1)
    actions = ActionChains(driver)
    # Simulate scrolling on the search page

    
    parent_handle = driver.window_handles[0]
    organizations_href = ""
    # Найти элемент

    # Получить размеры элемента
    
        
    scroller = Scroller(driver)   
    end_of_scroll = False
    try:
        while not end_of_scroll:
            end_of_scroll = scroller.scroll_element(".scroll__scrollbar-thumb", 0, 100)
            
        # Получение ссылок после завершения скроллинга
        organizations_href = driver.find_elements(By.CLASS_NAME, "search-snippet-view__link-overlay")
        print(len(organizations_href))
        database.connect()
        for href in organizations_href:  
            
            link = href.get_attribute("href")   
            name  = href.text
            database.insert_organization(name=name, link=link)
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

        

    
    
 


 

