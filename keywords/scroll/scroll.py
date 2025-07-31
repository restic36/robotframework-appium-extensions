from appium.webdriver.common.appiumby import AppiumBy
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

class scroll:
    # Defines the scope of the library as GLOBAL, making it shared across all tests
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        # Initializes BuiltIn to allow access to Robot Framework core functions
        self._builtin = BuiltIn()

    @property
    def driver(self):
        """
        Returns the current Appium driver instance managed by AppiumLibrary.
        This is necessary to interact directly with the mobile device.
        """
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    @keyword("Scroll Inside")
    def scroll_element(self, **kwargs):
        """
        Performs a swipe gesture inside a given element located by any supported Appium strategy.

        Accepts the following keyword arguments (Robot Framework style):
        - A locator key-value pair (e.g., xpath=..., id=..., accessibility_id=...)
        - direction (str): 'up', 'down', 'left', or 'right'. Default: 'down'
        - percent (float): Proportional distance of the swipe (0.01 to 1.0). Default: 0.75
        - speed (int): Swipe speed in pixels per second. Default: 800

        Example usage in Robot Framework:
            Scroll Inside    xpath=//android.widget.TextView[@text="Scroll Here"]    direction=down    percent=0.6
        """

        # Mapping of supported locator strategies to AppiumBy constants
        locator_strategies = {
            "id": AppiumBy.ID,
            "xpath": AppiumBy.XPATH,
            "accessibility_id": AppiumBy.ACCESSIBILITY_ID,
            "class_name": AppiumBy.CLASS_NAME,
            "android_uiautomator": AppiumBy.ANDROID_UIAUTOMATOR,
            "ios_predicate": AppiumBy.IOS_PREDICATE,
            "ios_class_chain": AppiumBy.IOS_CLASS_CHAIN,
            "name": AppiumBy.NAME
        }

        # Determine locator type and value from keyword arguments
        locator_type = None
        locator_value = None
        for key in kwargs:
            if key.lower() in locator_strategies:
                locator_type = key.lower()
                locator_value = kwargs[key]
                break

        if not locator_type or not locator_value:
            raise ValueError("You must specify a valid locator as a named argument (e.g., xpath=..., id=...).")

        # Read additional parameters with default values
        direction = kwargs.get("direction", "down")
        percent = float(kwargs.get("percent", 0.75))
        speed = int(kwargs.get("speed", 800))

        # Validate inputs
        if direction not in ["up", "down", "left", "right"]:
            raise ValueError("The 'direction' argument must be one of: 'up', 'down', 'left', 'right'.")
        if not (0.01 <= percent <= 1.0):
            raise ValueError("The 'percent' argument must be between 0.01 and 1.0.")
        if speed <= 0:
            raise ValueError("The 'speed' argument must be a positive integer.")

        try:
            # Get the Appium driver instance and locate the element
            driver = self.driver
            strategy = locator_strategies[locator_type]
            element = driver.find_element(strategy, locator_value)

            # Execute swipe gesture inside the located element
            driver.execute_script("mobile: swipeGesture", {
                "elementId": element.id,
                "direction": direction,
                "percent": percent,
                "speed": speed
            })

            # Log success in Robot Framework
            self._builtin.log(
                f"[SUCCESS] Scroll performed using {locator_type}='{locator_value}' with direction='{direction}', percent={percent}, speed={speed}.",
                "INFO"
            )

        except Exception as e:
            # Log and raise error in case of failure
            self._builtin.log(f"[ERROR] Failed to perform scroll: {str(e)}", "ERROR")
            raise
