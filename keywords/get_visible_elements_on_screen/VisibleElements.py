from robot.api.deco import keyword
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, WebDriverException
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.by import By
import json


class VisibleElements:
    """
    Custom AppiumLibrary keyword that returns visible elements on the screen with valid resource IDs, filtered by type.
    Useful for visual validation in mobile automation tests.
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'


    def __init__(self):
        self._builtin = BuiltIn()

    def _get_appium_driver(self):
    # Gets the current Appium driver instance
        appium_lib = self._builtin.get_library_instance("AppiumLibrary")
        return appium_lib._current_application()
    
    def _find_all_elements(self, driver):
    # Return all elements in the current screen using a generic XPath
        return driver.find_elements(By.XPATH, "//*")

    def _passes_filter(self, el, filter_type):
    # Check if the element matches the given filter type
        """Args:
            el (WebElement): the element to evaluate.
            filter_type (str): filter type options ('all' | 'clickable' | 'text' | 'button' | 'input').

        Returns:
            bool: Returns True if the element passes the filter, False otherwise."""
        
        class_name = el.get_attribute("class") or ""
        text = el.text or ""
        clickable = el.get_attribute("clickable") == "true"

        if filter_type == "all":
            return True
        if filter_type == "clickable":
            return clickable
        if filter_type == "text":
            # Uses strip() to ignore blank spaces
            return bool(text.strip())
        if filter_type == "button":
            return "Button" in class_name
        if filter_type == "input":
            return "EditText" in class_name
        # Returns False in case of an unrecognized filter (should not occur due to prior validation)
        return False

    def _build_debug_dict(self, el, rid):
    # Build a structured dictionary of element attributes for debug mode
        """Args:
            el (WebElement): the element that passed the filters.
            rid (str): the 'resource-id' of the element.

        Returns:
            dict: Structured data for debugging and inspection.
        """
        
        return {
            "resource_id": rid,
            "accessibility_id": el.get_attribute("content-desc") or "null",
            "text": el.text or "",
            "class": el.get_attribute("class") or "",
            "clickable": el.get_attribute("clickable") == "true"
        }

    @keyword("Get Visible Elements On Screen")
    def get_visible_elements_on_screen(self, filter_type: str = "all", debug: bool = False):
        """
        Return visible screen elements with valid resource IDs, optionally filtered by type.

        Args:
            filter_type (str): Filter to apply. Options: 'all' | 'clickable' | 'text' | 'button' | 'input'.
            debug (bool): If debug=True, return full element details as JSON; otherwise, return a list of IDs.

        Returns:
            list: List of filtered visible elements.
        """

        valid_filters = {'all', 'clickable', 'text', 'button', 'input'}
        # Normalize input to lowercase (lower()) and strip (strip()) spaces to avoid typos
        filter_type = filter_type.strip().lower()
        if filter_type not in valid_filters:
            self._builtin.fail(f"Invalid filter '{filter_type}'. Options: {valid_filters}")

        driver = self._get_appium_driver()
        try:
            elements = self._find_all_elements(driver)
        except WebDriverException as e:
            self._builtin.log(f"Error fetching elements: {e}", level="ERROR")
            return []
        
        self._builtin.log(f"Found {len(elements)} elements before filtering", level="DEBUG")

        visible_elements = []
        for el in elements:
            try:
                # First filter: real visibility
                if not el.is_displayed():
                    continue

                # Second filter: must have resource_id
                res_id = el.get_attribute("resource-id")
                if not res_id or not res_id.strip() or res_id.strip().lower() == "null":
                    continue
                rid = res_id.strip()

                # Third filter: match element type
                if not self._passes_filter(el, filter_type):
                    continue 

                # Define return format
                if debug:
                    # debug mode
                    visible_elements.append(self._build_debug_dict(el, rid))
                else:
                    # normal mode
                    visible_elements.append(rid)

            # Ignore elements that are no longer valid
            except (StaleElementReferenceException, NoSuchElementException) as ex:
            # NoSuchElementException: the element does not exist (e.g., invalid selector or not rendered yet)
            # StaleElementReferenceException: the element is no longer attached to the DOM (e.g., dynamic re-render)
                self._builtin.log(f"Ignored element due to {type(ex).__name__}: {ex}", level="DEBUG")
                continue

        # Log total elements that passed all filters
        count = len(visible_elements)
        self._builtin.log (f"Total visible elements after filtering: {count}", level="INFO")

        if debug:
            debug_output = json.dumps(visible_elements, indent=2)
            self._builtin.log("DEBUG JSON:\n" + debug_output, level="INFO")

        else:
            self._builtin.log("Visible elements:\n" + json.dumps(visible_elements, indent=2), level="INFO")
        return visible_elements