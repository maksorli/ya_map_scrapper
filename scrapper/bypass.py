import time
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from twocaptcha import TwoCaptcha
from config import api_key

# Global dictionary to store captcha results
dict_result = {}

def sender_solve(path):
    """
    Sends an image to the 2captcha API for solving and returns the solved captcha code.

    :param path: Path to the captcha image
    :return: Solved captcha code
    """
    solver = TwoCaptcha(api_key)
    print('2) Image sent for solving:')
    result = solver.normal(path, param='ru')
    print('3) Response received from API: ', result)
    # API returns a dictionary {'captchaId': '72447681441', 'code': 'gbkd'}
    # Update the dictionary to extract captcha ID and send a report
    dict_result.update(result)
    return result['code']

def main():
    """
    Main function to automate the process:
    1. Set up the web driver.
    2. Open the web page and interact with the captcha.
    3. Send the captcha image to 2captcha and enter the received code.
    4. Extract data after solving the captcha.
    """
    ua = UserAgent()
    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument('user-data-dir=C:\\User_Data')
    options_chrome.add_argument(f"--user-agent={ua}")

    with webdriver.Chrome(options=options_chrome) as browser:
        browser.implicitly_wait(15)  # Set implicit wait time to 15 seconds
        url = f'https://captcha-parsinger.ru/yandex?page=3'
        browser.get(url)

        # Switch to the captcha iframe
        WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='SmartCaptcha checkbox widget']")))

        # Wait for the button and click it
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[class="CheckboxCaptcha-Button"]'))).click()

        # Switch back to the main content
        browser.switch_to.default_content()

        # Switch to the new iframe with the image
        WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='SmartCaptcha advanced widget']")))

        # Hardcode the image name
        img_name = 'img_yandex.png'
        with open(img_name, 'wb') as file:
            # Extract the src attribute from the tag containing the image URL
            img = browser.find_element(By.CSS_SELECTOR, 'img[class="AdvancedCaptcha-Image"]').get_attribute('src')
            # Make a simple requests call to download the image and save it to a file
            file.write(requests.get(img).content)
            print(f'1) URL image: {img}')

        # Send the image for solving
        sender_solve(img_name)
        print(f'4) {dict_result["code"]}')
        # Enter the solved captcha code
        browser.find_element(By.CSS_SELECTOR, 'input[class="Textinput-Control"]').send_keys(dict_result['code'])
        
        # Switch back to the main content to extract articles
        browser.switch_to.default_content()
        
        # Click the submit button
        browser.find_element(By.CSS_SELECTOR, 'button[class="CaptchaButton CaptchaButton_view_action"]').click()

        # Enjoy the result for 10 seconds =)
        time.sleep(10)

