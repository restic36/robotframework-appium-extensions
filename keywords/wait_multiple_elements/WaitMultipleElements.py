from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import time

class WaitMultipleElements:
    """Class to wait for multiple elements simultaneously."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    @keyword("Wait Multiple Elements")
    def wait_multiple_elements(self, elements_list, timeout=10, wait_for_all=True, polling_interval=0.5):
        """
        Waits for multiple elements to be visible.

        Args:
            elements_list (list): List of element locators
            timeout (int): Maximum time to wait in seconds
            wait_for_all (bool): If True, waits for ALL elements; if False, waits for ANY element
            polling_interval (float): Time between checks in seconds
        
        Returns:
            dict: Dictionary with locator as key and visibility status as value
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
            
            self._builtin.log(f"Starting wait for {len(elements_list)} elements to be visible (wait_for_all={wait_for_all}, timeout={timeout}s)", level='INFO')
            
            results = {}
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                visible_elements = 0
                
                for locator in elements_list:
                    try:
                        element = appium_lib._element_find(locator, True, False)
                        if element and element.is_displayed():
                            results[locator] = True
                            visible_elements += 1
                            self._builtin.log(f"Element visible: {locator}", level='DEBUG')
                        else:
                            results[locator] = False
                    except Exception:
                        results[locator] = False
                
                # Check success conditions
                if wait_for_all and visible_elements == len(elements_list):
                    self._builtin.log(f"All {len(elements_list)} elements are visible", level='INFO')
                    return results
                elif not wait_for_all and visible_elements > 0:
                    self._builtin.log(f"{visible_elements} out of {len(elements_list)} elements are visible", level='INFO')
                    return results
                
                time.sleep(polling_interval)
            
            # Timeout reached
            visible_count = sum(1 for status in results.values() if status)
            
            if wait_for_all:
                raise TimeoutError(f"Timeout waiting for all elements to be visible. Found {visible_count}/{len(elements_list)} visible elements within {timeout}s")
            else:
                if visible_count == 0:
                    raise TimeoutError(f"Timeout waiting for any element to be visible. No visible elements found within {timeout}s")
                else:
                    return results
                    
        except Exception as e:
            if isinstance(e, (TimeoutError, ValueError, RuntimeError)):
                raise
            raise RuntimeError(f"Error waiting for multiple elements visibility: {str(e)}")