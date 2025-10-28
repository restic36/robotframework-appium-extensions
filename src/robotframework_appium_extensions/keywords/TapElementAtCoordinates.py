import time

from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


class TapElementAtCoordinates:
    """
    Library for performing clicks on elements at specific coordinates using Appium and W3C Actions.
    Supports both percentage and pixel offsets for flexible mobile automation.
    """

    def __init__(self):
        """
        Initializes the Appiumclick library and sets up the BuiltIn instance.
        """
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        """
        Returns the current Appium driver instance from AppiumLibrary.
        """
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    @keyword("Tap Element At Coordinates")
    def tap_element_at_coordinates(self, locator, xoffset=0.5, yoffset=0.5):
        """Click on mobile element at specified coordinates using touch actions.
        Supports percentage or pixel offsets from element's top-left corner.

        [Arguments]
        locator    Element locator string (id=submit, xpath=//button, etc)
        xoffset    Horizontal offset from left edge (default 0.5)
                  Values 0-1: percentage of element width
                  Values >1: absolute pixels from left
        yoffset    Vertical offset from top edge (default 0.5)
                  Values 0-1: percentage of element height 
                  Values >1: absolute pixels from top

        [Returns]
        None. Keyword passes if click action completes successfully.

        [Raises]
        RuntimeError    When Appium driver is not initialized
        ValueError     When element is not found
                      When offsets are not valid numbers
                      When click position is outside screen
        """
        driver = self._driver
        appium_lib = self._builtin.get_library_instance("AppiumLibrary")

        self._builtin.log("Checking if driver is active", level="INFO")
        if not driver:
            raise RuntimeError("Driver is not initialized or not connected to the device.")

        self._builtin.log(f"Searching for element with locator: {locator}", level="INFO")
        try:
            element = appium_lib.get_webelement(locator)
        except Exception as e:
            raise ValueError(f"Element with locator '{locator}' not found: {e}")

        location = element.location
        size = element.size
        self._builtin.log(f"Element location: {location}, Size: {size}", level="INFO")

        try:
            xoffset = float(xoffset)
            yoffset = float(yoffset)
        except Exception:
            raise ValueError("xoffset and yoffset must be numbers (e.g., 0.5 for percentage or 30 for pixels)")

        # If offset is between 0 and 1, treat as percentage
        if 0 <= xoffset <= 1:
            xoffset_px = int(size["width"] * xoffset)
        else:
            xoffset_px = int(xoffset)

        if 0 <= yoffset <= 1:
            yoffset_px = int(size["height"] * yoffset)
        else:
            yoffset_px = int(yoffset)

        # Final click coordinate on the screen
        x = location["x"] + xoffset_px
        y = location["y"] + yoffset_px
        self._builtin.log(
            f"Calculated click coordinates: ({x}, {y}) (offsets: {xoffset_px}, {yoffset_px})", level="INFO"
        )

        # Check if within screen bounds
        window_size = driver.get_window_size()
        self._builtin.log(f"Screen size: {window_size}", level="INFO")

        if not (0 <= x <= window_size["width"] and 0 <= y <= window_size["height"]):
            raise ValueError(f"Coordinates ({x}, {y}) are out of device screen bounds.")

        try:
            self._builtin.log("Performing click using W3C Actions", level="INFO")
            touch = PointerInput("touch", "finger")
            actions = ActionBuilder(driver, mouse=touch)

            actions.pointer_action.move_to_location(x, y)
            actions.pointer_action.pointer_down()
            time.sleep(0.2)
            actions.pointer_action.pointer_up()

            actions.perform()
            self._builtin.log("Click performed successfully via W3C Actions", level="INFO")
        except Exception as e:
            self._builtin.log(f"Error performing W3C Actions: {e}", level="ERROR")
            raise
