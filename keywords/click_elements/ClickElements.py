from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
import time

class ClickElements:
    """Class to execute sequential clicks on multiple elements."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    @keyword("Click Elements")
    def click_elements(self, elements_list, click_duration=100, interval_between_clicks=0.5):
        """
        Clicks sequentially on multiple elements.

        Args:
            elements_list (list): List of element locators
            click_duration (int): Click duration in milliseconds
            interval_between_clicks (float): Interval between clicks in seconds
        """
        if not isinstance(elements_list, list):
            raise ValueError("elements_list must be a list of locators")
        
        if not elements_list:
            raise ValueError("The elements list cannot be empty")

        try:
            driver = self._driver
            if not driver:
                raise RuntimeError("Appium driver is not available")

            appium_lib = self._builtin.get_library_instance("AppiumLibrary")
            
            self._builtin.log(f"Starting sequential click on {len(elements_list)} elements", level='INFO')
            
            for i, locator in enumerate(elements_list, 1):
                self._builtin.log(f"Clicking element {i}/{len(elements_list)}: {locator}", level='INFO')
                
                # Find element
                element = appium_lib._element_find(locator, True, True)
                if not element:
                    self._builtin.log(f"Element not found: {locator}", level='WARN')
                    continue
                
                # Get location and size
                location = element.location
                size = element.size
                
                # Calculate center coordinates
                center_x = location['x'] + size['width'] / 2
                center_y = location['y'] + size['height'] / 2
                
                # Execute click
                actions = ActionChains(driver)
                touch = actions.w3c_actions.add_pointer_input('touch', 'finger')
                
                touch.create_pointer_move(x=center_x, y=center_y)
                touch.create_pointer_down(button=0)
                touch.create_pause(click_duration / 1000)
                touch.create_pointer_up(button=0)
                
                actions.perform()
                
                self._builtin.log(f"Click executed on element {i}: {locator}", level='INFO')
                
                # Pause between clicks (except for the last one)
                if i < len(elements_list):
                    time.sleep(interval_between_clicks)
                    
        except Exception as e:
            raise RuntimeError(f"Error executing multiple clicks: {str(e)}")