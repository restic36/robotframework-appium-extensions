from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton

class TapAtPercentage:
    """Class to tap at a specific point on the screen using percentage coordinates."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    @keyword("Tap At Percentage")
    def tap_at_percentage(self, x, y, duration=100):
        """
        Taps at a specific point on the screen using percentage coordinates.

        Args:
            x (float): X coordinate as a percentage of the screen (0.0 to 1.0).
            y (float): Y coordinate as a percentage of the screen (0.0 to 1.0).
            duration (int): Duration of the tap in milliseconds.
        """
        try:
            x = float(x)
            y = float(y)
        except ValueError:
            raise ValueError("Arguments 'x' and 'y' must be numbers (float).")
        
        if not (0.0 <= x <= 1.0) or not (0.0 <= y <= 1.0):
            raise ValueError("Arguments 'x' and 'y' must be percentages between 0.0 and 1.0.")

        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("Argument 'duration' must be a positive integer.")

        try:
            driver = self._driver
            if not driver:
                raise RuntimeError("Appium driver is not available.")

            screen_size = driver.get_window_size()
            screen_width = screen_size['width']
            screen_height = screen_size['height']

            x_px = int(screen_width * x)
            y_px = int(screen_height * y)

            self._builtin.log(f"Tapping at ({x_px}, {y_px}) [percentages: ({x}, {y})]", level='INFO')

            actions = ActionChains(driver)
            touch = actions.w3c_actions.add_pointer_input('touch', 'finger')
            touch.create_pointer_move(x=x_px, y=y_px)
            touch.create_pointer_down(button=MouseButton.LEFT)
            touch.create_pause(duration / 1000)
            touch.create_pointer_up(button=MouseButton.LEFT)
            actions.perform()

            self._builtin.log(f"Tap performed at ({x_px}, {y_px})", level='INFO')
            return True

        except Exception as e:
            raise RuntimeError(f"Error performing tap: {str(e)}")