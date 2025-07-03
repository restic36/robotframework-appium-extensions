from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains
import random

class AppiumZoomExtensions:
    """Class for Zoom in movement in Appium"""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def _driver(self):
        return self._builtin.get_library_instance("AppiumLibrary")._current_application()

    @keyword("Perform Zoom")
    def perform_zoom_in_gesture(self, locator, scale=1.5, duration=500, direction="vertical", pause_s=0.1, steps=50):
        """
        Performs a zoom in gesture on an Android application.

        Args:
            locator (str): Element locator.
            scale (float): Gesture scale (must be > 1.0).
            duration (int): Total movement duration in milliseconds.
            direction (str): "vertical" or "horizontal".
            pause_s (float): Pause in seconds before movement begins.
            steps (int): Number of interpolation steps with perturbation.
        """
        if not isinstance(locator, str) or not locator:
            raise ValueError("The 'locator' argument must be a non-empty string.")
        if scale <= 1.0:
            raise ValueError("The 'scale' argument must be greater than 1.0 for Zoom In.")
        if duration <= 0:
            raise ValueError("The 'duration' must be a positive integer.")
        if direction.lower() not in ["vertical", "horizontal"]:
            raise ValueError("Direction must be 'vertical' or 'horizontal'.")

        try:
            driver = self._driver
            if not driver:
                raise RuntimeError("The Appium driver is not available.")

            screen_size = driver.get_window_size()
            screen_width = screen_size['width']
            screen_height = screen_size['height']

            appium_lib = self._builtin.get_library_instance("AppiumLibrary")
            element = appium_lib._element_find(locator, True, True)
            if not element:
                raise RuntimeError(f"Element not found for locator: {locator}")

            location = element.location
            x, y = location['x'], location['y']
            width, height = element.size['width'], element.size['height']
            center_x, center_y = x + width / 2, y + height / 2

            offset = 10
            movement = center_y * (scale - 1) if direction == "vertical" else center_x * (scale - 1)

            if direction == "vertical":
                f1_start = (center_x, center_y - offset)
                f1_end = (center_x, center_y - movement)
                f2_start = (center_x, center_y + offset)
                f2_end = (center_x, center_y + movement)
            else:
                f1_start = (center_x - offset, center_y)
                f1_end = (center_x - movement, center_y)
                f2_start = (center_x + offset, center_y)
                f2_end = (center_x + movement, center_y)

            def adjust(x, y):
                return max(0, min(x, screen_width)), max(0, min(y, screen_height))

            f1_start = adjust(*f1_start)
            f1_end = adjust(*f1_end)
            f2_start = adjust(*f2_start)
            f2_end = adjust(*f2_end)

            actions = ActionChains(driver)
            finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
            finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

            # Volta para posição inicial
            finger1.create_pointer_move(x=f1_start[0], y=f1_start[1])
            finger2.create_pointer_move(x=f2_start[0], y=f2_start[1])

            # Posiciona os dois dedos na tela (com button=0)
            finger1.create_pointer_down(button=0)
            finger2.create_pointer_down(button=0)

            # Aguarda um tempo 'pause_s' antes de mover
            finger1.create_pause(pause_s)
            finger2.create_pause(pause_s)

           
            for i in range(1, steps + 1):
                t = i / steps #Steps define o quanto o movimento será dividido. Para movimentos curtos (scale baixo), recomenda-se steps de 10 a 20
                #Para movimentos longos (scale alto), recomenda-se steps de 50
                interp_f1_x = f1_start[0] + t * (f1_end[0] - f1_start[0]) + random.uniform(-0, 0)
                interp_f1_y = f1_start[1] + t * (f1_end[1] - f1_start[1]) + random.uniform(-0, 0)
                interp_f2_x = f2_start[0] + t * (f2_end[0] - f2_start[0]) + random.uniform(-0, 0)
                interp_f2_y = f2_start[1] + t * (f2_end[1] - f2_start[1]) + random.uniform(-0, 0)

                interp_f1_x, interp_f1_y = adjust(interp_f1_x, interp_f1_y)
                interp_f2_x, interp_f2_y = adjust(interp_f2_x, interp_f2_y)

                move_duration = int(duration / steps) # Duração de cada fragmento de pertubação

                finger1.create_pointer_move(x=interp_f1_x, y=interp_f1_y, duration=move_duration)
                finger2.create_pointer_move(x=interp_f2_x, y=interp_f2_y, duration=move_duration)

            # Levanta os dedos, encerrando o movimento
            finger1.create_pointer_up(button=0)
            finger2.create_pointer_up(button=0)

            actions.perform()

        except Exception as e:
            raise RuntimeError(f"Error while performing the zoom in gesture: {str(e)}")
