"""
Scroll Element Library
======================

Custom Robot Framework library for performing scroll (swipe) gestures inside scrollable
elements in mobile applications using Appium.

Overview
--------
- Supports locating elements by various strategies: id, xpath, accessibility_id,
  class_name, android_uiautomator, ios_predicate, ios_class_chain, name.
- Performs scroll gestures in four directions: up, down, left, right.
- Configurable scroll distance via `percent` (0.01 to 1.0).
- Adjustable gesture speed (milliseconds).
- Validates input parameters and logs detailed success or error messages.

Requirements
------------
- Python 3.7+
- Appium Server configured and running
- Robot Framework:
    pip install robotframework
- AppiumLibrary:
    pip install robotframework-appiumlibrary

Import in Robot Framework
-------------------------
Library    scroll.py
Library    AppiumLibrary

Usage
-----
Scroll Inside    <locator>    direction=<up|down|left|right>    percent=<0.01-1.0>    speed=<ms>

Examples
--------
Scroll Inside    xpath=//android.widget.ScrollView    direction=down    percent=0.75    speed=800
Scroll Inside    id=com.example:id/list              direction=up      percent=0.5     speed=600
Scroll Inside    accessibility_id=MyScrollable      direction=left    percent=0.8     speed=700

Parameters
----------
locator   (str)   Target element locator (required).
direction (str)   Scroll direction. Default: "down".
percent   (float) Scroll distance as a percentage of the element size. Default: 0.75.
speed     (int)   Gesture speed in milliseconds. Default: 800.

Notes
-----
- Throws exception if element is not found or parameters are invalid.
- Uses Appium's `mobile: swipeGesture` command internally.
"""


from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

# Defines the custom keyword class
class scroll:
    # Defines the library scope as GLOBAL (same instance will be reused across all tests)
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        # Access to Robot Framework's BuiltIn library (for functions like Log, Set Test Variable, etc.)
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        # Retrieves the current Appium driver instance from AppiumLibrary
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    @keyword("Scroll Inside")
    def scroll_element(self, *args, **kwargs):
        """
        Performs a scroll (swipe) gesture inside a scrollable element identified by XPath, ID, accessibility_id, etc.

        Usage examples:
        - Scroll Inside    xpath=//my/xpath    direction=down
        - Scroll Inside    //my/xpath          direction=down
        - Scroll Inside    ${my_element}       direction=down
        """

        locator = None  # Will hold the final locator string

        # List of supported locator strategies
        locator_keys = [
            "id", "xpath", "accessibility_id", "class_name",
            "android_uiautomator", "ios_predicate", "ios_class_chain", "name"
        ]

        # Attempt to extract locator from keyword arguments (e.g., xpath=..., id=...)
        for key in kwargs:
            if key.lower() in locator_keys:
                locator = f"{key.lower()}={kwargs[key]}"
                break

        # If no locator found from kwargs, check positional argument
        if not locator and args:
            locator = args[0].strip()
            # Check if already in valid format (e.g., id=..., xpath=...)
            if not any(locator.startswith(f"{prefix}=") for prefix in locator_keys):
                # If starts with //, assume it’s a raw XPath
                if locator.startswith("//"):
                    locator = f"xpath={locator}"
                else:
                    locator = None  # Invalid format

        # If still no valid locator, raise an error
        if not locator:
            raise ValueError("You must provide a valid locator: 'xpath=...', 'id=...', 'accessibility_id=...', or just '//...'.")

        # Read optional parameters
        direction = kwargs.get("direction", "down")       # Scroll direction
        percent = float(kwargs.get("percent", 0.75))      # Scroll percentage (0.01 to 1.0)
        speed = int(kwargs.get("speed", 800))             # Gesture speed in milliseconds

        # Validate direction and limits
        if direction not in ["up", "down", "left", "right"]:
            raise ValueError("direction must be one of: 'up', 'down', 'left', or 'right'")
        if not (0.01 <= percent <= 1.0):
            raise ValueError("percent must be between 0.01 and 1.0")
        if speed <= 0:
            raise ValueError("speed must be a positive integer")

        try:
            # Get driver and AppiumLibrary instance
            driver = self._driver
            appium_lib = self._builtin.get_library_instance("AppiumLibrary")

            # Find the element on screen using the provided locator
            element = appium_lib._element_find(locator, True, True)
            if not element:
                raise Exception(f"Element not found using locator: {locator}")

            # Adjust only vertical directions (Appium interprets as finger movement)
            gesture_direction = direction
            if direction == "down":
                gesture_direction = "up"    # To scroll content down, finger goes up
            elif direction == "up":
                gesture_direction = "down"  # To scroll content up, finger goes down

            driver.execute_script("mobile: swipeGesture", {
                "elementId": element.id,
                "direction": gesture_direction,
                "percent": percent,
                "speed": speed
            })

            # Log success message
            self._builtin.log(
                f"[SUCCESS] Scroll performed with locator='{locator}', direction='{direction}', percent={percent}, speed={speed}",
                "INFO"
            )

        except Exception as e:
            # Log error and raise it so Robot Framework can handle it properly
            self._builtin.log(f"[ERROR] Scroll failed: {str(e)}", "ERROR")
            raise