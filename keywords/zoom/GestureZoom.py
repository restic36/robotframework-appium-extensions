from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
import warnings
import random


class GestureZoom:
    """Custom Gesture Extension Class for AppiumLibrary with enhanced zoom gesture."""
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def driver(self):
        # Retrieves the current Appium driver instance from AppiumLibrary
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    def _get_element_center(self, locator):
        # Identifies the element and calculates its center point
        appium_lib = self._builtin.get_library_instance("AppiumLibrary")
        element = appium_lib._element_find(locator, True, True)
        if not element:
            raise RuntimeError(f"Element not found for locator: {locator}")
        location = element.location
        size = element.size
        x, y = location['x'], location['y']
        width, height = size['width'], size['height']
        return x + width / 2, y + height / 2, element

    def _calculate_finger_final_positions(self, x, y, scale, movement, direction):
        # Defines the final finger positions based on gesture center, scale, and movement range
        displacement = scale * movement
        if direction.lower() == "vertical":
            return (x, y - displacement), (x, y + displacement)
        else:
            return (x - displacement, y), (x + displacement, y)

    def _adjust_to_screen_bounds(self, positions, screen_width, screen_height):
        # Ensures finger coordinates are within screen bounds
        adjusted_positions = []
        for x, y in positions:
            new_x = max(0, min(x, screen_width))
            new_y = max(0, min(y, screen_height))
            if (x, y) != (new_x, new_y):
                warnings.warn(
                    f"Finger position ({x}, {y}) adjusted to ({new_x}, {new_y}) to fit within screen bounds.")
            adjusted_positions.append((new_x, new_y))
        return adjusted_positions

    def _validate_zoom_args(self, locator, scale, duration, direction, movement):
        # Validates gesture arguments for correctness and safety
        if locator is not None:
            if not isinstance(locator, str) or not locator:
                raise ValueError("The 'locator' must be a non-empty string.")
            if '=' not in locator:
                raise ValueError(f"Locator '{locator}' must be in the format 'strategy=value'")
        if scale <= 1.0:
            raise ValueError("Scale must be greater than 1.0")
        if duration <= 0:
            raise ValueError("Duration must be a positive integer.")
        if direction.lower() not in ["vertical", "horizontal"]:
            raise ValueError("Direction must be 'vertical' or 'horizontal'.")
        if movement <= 0:
            raise ValueError("Movement must be positive")

    @keyword("Perform Zoom Gesture")
    def perform_zoom_gesture(self, locator=None, scale=1.5, duration=500, direction="vertical", movement=300, pause=0.1, steps=50):
        """
        Performs a realistic zoom gesture with perturbation.

        Args:
            locator (str): Element locator (optional; if None, uses screen center).
            scale (float): Gesture scale (> 1.0).
            duration (int): Total duration of the gesture in milliseconds.
            direction (str): Gesture direction ("vertical" or "horizontal").
            movement (int/float): Gesture amplitude in pixels.
            pause (int/float): Pause in seconds before movement begins.
            steps (int): Number of interpolation steps for gesture realism.
        """

        self._validate_zoom_args(locator, scale, duration, direction, movement)

        try:
            driver = self.driver
            if not driver:
                raise RuntimeError("The Appium driver is not available.")

            screen_size = driver.get_window_size()
            screen_width = screen_size['width']
            screen_height = screen_size['height']

            if locator is None:
                center_x = screen_width / 2
                center_y = screen_height / 2
                self._builtin.log("No locator provided. Using center of the screen.", "INFO")
            else:
                center_x, center_y, _ = self._get_element_center(locator)
                self._builtin.log(f"Element center at ({center_x}, {center_y})", "INFO")

            offset = 10
            f1_start = (center_x, center_y - offset) if direction == "vertical" else (center_x - offset, center_y)
            f2_start = (center_x, center_y + offset) if direction == "vertical" else (center_x + offset, center_y)

            f1_end, f2_end = self._calculate_finger_final_positions(center_x, center_y, scale, movement, direction)

            f1_start, f1_end, f2_start, f2_end = self._adjust_to_screen_bounds(
                [f1_start, f1_end, f2_start, f2_end], screen_width, screen_height)

            self._builtin.log(f"Finger 1 starts at ({f1_start})", "INFO")
            self._builtin.log(f"Finger 2 starts at ({f2_start})", "INFO")

            actions = ActionChains(driver)
            actions.w3c_actions.devices = []
            finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
            finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

            finger1.create_pointer_move(x=f1_start[0], y=f1_start[1])
            finger2.create_pointer_move(x=f2_start[0], y=f2_start[1])

            finger1.create_pointer_down(button=MouseButton.LEFT)
            finger2.create_pointer_down(button=MouseButton.LEFT)

            finger1.create_pause(pause)
            finger2.create_pause(pause)

            for i in range(1, steps + 1):
                t = i / steps
                interp_f1_x = f1_start[0] + t * (f1_end[0] - f1_start[0]) + random.uniform(-0.0, 0.0)
                interp_f1_y = f1_start[1] + t * (f1_end[1] - f1_start[1]) + random.uniform(-0.0, 0.0)
                interp_f2_x = f2_start[0] + t * (f2_end[0] - f2_start[0]) + random.uniform(-0.0, 0.0)
                interp_f2_y = f2_start[1] + t * (f2_end[1] - f2_start[1]) + random.uniform(-0.0, 0.0)

                interp_f1_x, interp_f1_y = max(0, min(interp_f1_x, screen_width)), max(0, min(interp_f1_y, screen_height))
                interp_f2_x, interp_f2_y = max(0, min(interp_f2_x, screen_width)), max(0, min(interp_f2_y, screen_height))

                move_duration = int(duration / steps)
                finger1.create_pointer_move(x=interp_f1_x, y=interp_f1_y, duration=move_duration)
                finger2.create_pointer_move(x=interp_f2_x, y=interp_f2_y, duration=move_duration)

            finger1.create_pointer_up(button=MouseButton.LEFT)
            finger2.create_pointer_up(button=MouseButton.LEFT)

            actions.perform()
            self._builtin.log("Zoom gesture performed successfully.", "INFO")

        except Exception as e:
            raise RuntimeError(f"Error while performing the zoom gesture: {str(e)}")
