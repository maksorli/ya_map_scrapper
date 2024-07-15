from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import MoveTargetOutOfBoundsException, NoSuchElementException
import time

class Scroller:
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)

    def scroll_element(self, css_selector, move_x, move_y, timeout=2, check_content_change=True):
        """
        Scrolls an element by a specified offset.

        Args:
        css_selector (str): CSS selector of the element to be scrolled.
        move_x (int): Horizontal offset to move.
        move_y (int): Vertical offset to move.
        timeout (int): Time to wait after scrolling.
        check_content_change (bool): Flag to check if content has changed after scroll.

        Returns:
        bool: True if end of scroll is reached or no content change, False otherwise.
        """
        try:
            slider = self.driver.find_element(By.CSS_SELECTOR, css_selector)
            last_content = None
            if check_content_change:
                last_content = self.get_visible_content()

            self.actions.click_and_hold(slider).move_by_offset(move_x, move_y).release().perform()
            time.sleep(timeout)  # Wait for content to load

            if check_content_change:
                new_content = self.get_visible_content()
                if new_content == last_content:
                    return True  # End of scroll or no change in content

            return False  # More content potentially available

        except (MoveTargetOutOfBoundsException, NoSuchElementException) as e:
            print(f"Error during scrolling: {e}")
            return True  # Assume end of scroll if error occurs

    def get_visible_content(self):
        """Returns the visible text content of the body tag."""
        return self.driver.find_element(By.TAG_NAME, "body").text