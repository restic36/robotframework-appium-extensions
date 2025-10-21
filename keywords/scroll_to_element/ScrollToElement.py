from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
import warnings
import time
import random


class ScrollToElement:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def driver(self):
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    def _adjust_to_screen_bounds(self, x, y, screen_width, screen_height):
        return max(0, min(x, screen_width)), max(0, min(y, screen_height))

    def _is_element_visible(self, locator):
        try:
            appium_lib = self._builtin.get_library_instance("AppiumLibrary")
            element = appium_lib._element_find(locator, True, True)
            return element.is_displayed()
        except:
            return False

    def _get_element_area_center(self, locator):
        appium_lib = self._builtin.get_library_instance("AppiumLibrary")
        element = appium_lib._element_find(locator, True, True)
        if not element:
            raise RuntimeError(f"Element not found for locator: {locator}")
        location = element.location
        size = element.size
        x, y = location['x'], location['y']
        width, height = size['width'], size['height']
        center_x = x + width / 2
        center_y = y + height / 2
        return x, y, width, height, center_x, center_y

    def _perform_scroll(self, start_x, start_y, end_x, end_y, duration=500, steps=20):
        driver = self.driver
        actions = ActionChains(driver)
        actions.w3c_actions.devices = []
        finger = actions.w3c_actions.add_pointer_input('touch', 'finger1')

        finger.create_pointer_move(x=start_x, y=start_y)
        finger.create_pointer_down(button=MouseButton.LEFT)
        finger.create_pause(0.05)

        for i in range(1, steps + 1):
            t = i / steps
            interp_x = start_x + t * (end_x - start_x) + random.uniform(-0, 0)
            interp_y = start_y + t * (end_y - start_y) + random.uniform(-0, 0)
            interp_x, interp_y = self._adjust_to_screen_bounds(
                interp_x, interp_y,
                driver.get_window_size()['width'],
                driver.get_window_size()['height']
            )
            move_duration = int(duration / steps)
            finger.create_pointer_move(x=interp_x, y=interp_y, duration=move_duration)

        finger.create_pointer_up(button=MouseButton.LEFT)
        actions.perform()

    @keyword("Scroll To Element")
    def scroll_into_element(self, locator, max_swipes=5, direction="down", swipe_distance_ratio=0.4,
                           duration=500, container_locator=None):
        """
        Swipes vertically or horizontally (optionally within a container element) until the target element is visible.

        Args:
            locator (str): Target element to find.
            max_swipes (int): Maximum number of swipes to attempt.
            direction (str): 'down', 'up', 'left', or 'right'.
            swipe_distance_ratio (float): Fraction of screen/container size to swipe (0.1 to 0.99).
            duration (int): Duration of the swipe in milliseconds.
            container_locator (str): Optional. Element within which the swipe should be confined.
        """
        direction = direction.lower()
        if direction not in ["down", "up", "left", "right"]:
            raise ValueError("Direction must be 'down', 'up', 'left', or 'right'.")
        if not (0.1 <= swipe_distance_ratio <= 0.99):
            raise ValueError("Swipe distance ratio must be between 0.1 and 0.99.")

        driver = self.driver
        screen_size = driver.get_window_size()
        screen_width = screen_size["width"]
        screen_height = screen_size["height"]

        if container_locator:
            self._builtin.log(f"Using swipe area from container: {container_locator}", "INFO")
            x, y, width, height, center_x, center_y = self._get_element_area_center(container_locator)
        else:
            self._builtin.log("Using entire screen for swipe", "INFO")
            x, y, width, height = 0, 0, screen_width, screen_height
            center_x = screen_width // 2
            center_y = screen_height // 2

        swipe_distance_x = swipe_distance_ratio * width
        swipe_distance_y = swipe_distance_ratio * height

        if direction == "down":
            start_x, end_x = center_x, center_x
            start_y = y + height // 2 + swipe_distance_y / 2
            end_y = y + height // 2 - swipe_distance_y / 2
        elif direction == "up":
            start_x, end_x = center_x, center_x
            start_y = y + height // 2 - swipe_distance_y / 2
            end_y = y + height // 2 + swipe_distance_y / 2
        elif direction == "right":
            start_y, end_y = center_y, center_y
            start_x = x + width // 2 + swipe_distance_x / 2
            end_x = x + width // 2 - swipe_distance_x / 2
        elif direction == "left":
            start_y, end_y = center_y, center_y
            start_x = x + width // 2 - swipe_distance_x / 2
            end_x = x + width // 2 + swipe_distance_x / 2

        start_x, start_y = int(start_x), int(start_y)
        end_x, end_y = int(end_x), int(end_y)

        for attempt in range(max_swipes):
            self._builtin.log(f"[SwipeAttempt {attempt + 1}] Trying to locate '{locator}'", "DEBUG")

            if self._is_element_visible(locator):
                self._builtin.log(f"Element '{locator}' found on attempt {attempt + 1}", "INFO")
                return

            self._builtin.log(f"Swiping from ({start_x}, {start_y}) to ({end_x}, {end_y})", "DEBUG")
            self._perform_scroll(start_x, start_y, end_x, end_y, duration=duration)
            time.sleep(0.5)

        raise RuntimeError(f"Element '{locator}' not found after {max_swipes} swipe attempts.")
