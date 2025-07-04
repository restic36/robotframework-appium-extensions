from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton

class TapAPoint:
    """Custom keyword set for absolute touch interactions using W3C Actions."""
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    def _validate_coordinates(self, x, y):
    # Validate input coordinates
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            raise ValueError("The 'x' and 'y' arguments must be integers.")
        return x, y

    def _validate_duration(self, duration):
    # Validate press duration
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("The 'duration' must be a positive integer.")
        return duration

    # Coordinate and duration validations are handled separately to improve clarity and reusability

    def _get_driver(self):
    # Retrieves the current Appium driver instance from AppiumLibrary
        appium_lib = self._builtin.get_library_instance("AppiumLibrary")
        return appium_lib._current_application()

    def _adjust_coordinates_to_screen_bounds(self, x, y, screen_width, screen_height):
    # Ensures coordinates are within screen boundaries
        original_x, original_y = x, y
        x = max(0, min(x, screen_width))
        y = max(0, min(y, screen_height))
        if (x, y) != (original_x, original_y):
            self._builtin.log(f"Coordinates adjusted from ({original_x}, {original_y}) to ({x}, {y}) to fit within screen bounds.", "WARN")
        return x, y

    @keyword("Tap A Point")
    # "Tap" is more appropriate than "Click" in mobile UI interactions and aligns with Appium standards.
    def perform_tap_a_point(self, x, y, duration=100):
        """
        Performs a tap gesture at an absolute screen coordinate.

        Args:
            x (int): X coordinate of the tap point.
            y (int): Y coordinate of the tap point.
            duration (int): Duration of the press in milliseconds.
        """
        # From this point forward, we'll follow a modular approach by consistently calling helper functions
        # to keep the main keyword logic clean, reusable, and easier to maintain

        driver = self._get_driver()
        if not driver:
            raise RuntimeError("Appium driver is not available.")
        
        x, y = self._validate_coordinates(x, y)
        duration = self._validate_duration(duration)

        # Get screen dimensions
        screen_size = driver.get_window_size()
        screen_width = screen_size['width']
        screen_height = screen_size['height']

        x, y = self._adjust_coordinates_to_screen_bounds(x, y, screen_width, screen_height)

        # Logs the exact action being performed to help with debugging and traceability
        self._builtin.log(f"Performing tap at ({x}, {y}) for {duration}ms", "INFO")

        # Create an instance of ActionChains
        actions = ActionChains(driver)
        # Define touch pointer
        touch = actions.w3c_actions.add_pointer_input('touch', 'finger')

        # Configure the tap action
        touch.create_pointer_move(x=x, y=y)
        touch.create_pointer_down(button=MouseButton.LEFT)
        # The "pause" function expects duration in seconds, so we convert the input from milliseconds (duration / 1000)
        touch.create_pause(duration / 1000)
        touch.create_pointer_up(button=MouseButton.LEFT)

        # Perform the actions
        actions.perform()