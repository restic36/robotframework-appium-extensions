from appium.webdriver.extensions.applications import Applications
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.extensions.applications import Applications
import re


class TerminateApplicationExtension:
    """
    Class to handle application termination in Appium
    This class provides keywords to terminate an application
    Additionally, it allows retrieval of the current application ID(appPackage) and activity(appActivity) for your own use.
    This is useful for testing scenarios where you need to ensure the application is closed
    If the application is not installed, a RuntimeError is expected to be raised at runtime.
    If the application is not currently running, a warning will be logged.
    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def driver(self):
        """Returns the current Appium driver instance."""
        try:
            return self._builtin.get_library_instance("AppiumLibrary")._current_application()
        except Exception as e:
            raise RuntimeError(
                f"Failed to get AppiumLibrary instance. Ensure AppiumLibrary is imported and a session is active. Error: {str(e)}"
            )

    @keyword("Terminate Application Extension")
    def terminate_application_extension(self, app_id):
        """
        Terminates the application specified by app_id.

        [Arguments]
        - app_id: The application package identifier (e.g., 'com.example.app')

        [Return Values]
        - Returns True if application was running and successfully terminated
        - Returns False if application was not running

        Note: The return value indicates the application state before termination:
        - True means the app was active and has been closed
        - False means the app was already closed or not running

        [Raises]
        - ValueError: If app_id is empty or invalid
        - RuntimeError: If driver is not available or termination fails

         [Example]
        | ${result}= | Terminate Application Extension | com.google.android.youtube |
        | Should Be True | ${result} | Application should have been running |
        """
        # Validate app_id parameter
        if not app_id:
            raise ValueError("app_id parameter cannot be empty")

        if not isinstance(app_id, str):
            raise TypeError(f"app_id must be a string, got {type(app_id).__name__}")

        app_id = app_id.strip()
        if not app_id:
            raise ValueError("app_id parameter cannot be empty or whitespace only")

        # Validate app_id format (basic Android package name validation)
        if not self._is_valid_package_name(app_id):
            raise ValueError(f"Invalid app_id format: '{app_id}'. Expected format: 'com.example.app'")

        try:
            driver = self.driver
            self._builtin.log(f"Attempting to terminate application: {app_id}", level="INFO")

            # Check if app is running before terminating
            if not driver.is_app_installed(app_id):
                raise RuntimeError(f"Application '{app_id}' is not installed on the device")

            # Debug log before terminate_app() execution
            self._builtin.log(f"DEBUG: Executing driver.terminate_app() for app_id='{app_id}'", level="DEBUG")
            self._builtin.log(f"DEBUG: Driver capabilities: {driver.desired_capabilities}", level="DEBUG")

            result = driver.terminate_app(app_id)

            if result:
                self._builtin.log(f"Successfully terminated application: {app_id}", level="INFO")
            else:
                self._builtin.log(f"Application '{app_id}' was not running or already terminated", level="WARN")

            return result

        except RuntimeError:
            # Re-raise RuntimeError with original message
            self._builtin.log(f"RuntimeError occurred while terminating '{app_id}'", level="ERROR")
            raise
        except Exception as e:
            self._builtin.log(f"Unexpected exception occurred while terminating '{app_id}': {type(e).__name__}", level="ERROR")
            raise RuntimeError(f"Failed to terminate application '{app_id}': {str(e)}")
        finally:
            # Log completion of termination attempt regardless of success or failure
            self._builtin.log(f"Termination attempt completed for application: {app_id}", level="DEBUG")

    @keyword("Get Current App Id")
    def get_current_app_id(self):
        """
        Returns the appPackage (app_id) of the current session.

        [Return Values]
        - Returns the application package identifier as a string

        [Raises]
        - RuntimeError: If driver is not available or app_id cannot be retrieved

        [Example]
        | ${app_id}= | Get Current App Id |
        | Log | Current app: ${app_id} |
        """
        try:
            driver = self.driver
            app_id = driver.desired_capabilities.get("appPackage")

            if not app_id:
                raise RuntimeError("Could not retrieve appPackage from current session. Session may not be active.")

            self._builtin.log(f"Current application ID: {app_id}", level="INFO")
            return app_id

        except RuntimeError:
            self._builtin.log("RuntimeError occurred while retrieving current app ID", level="ERROR")
            raise
        except Exception as e:
            self._builtin.log(f"Unexpected exception occurred while retrieving app ID: {type(e).__name__}", level="ERROR")
            raise RuntimeError(f"Failed to get current app ID: {str(e)}")
        finally:
            # Log completion of app ID retrieval attempt
            self._builtin.log("App ID retrieval attempt completed", level="DEBUG")

    def _is_valid_package_name(self, package_name):
        """
        Validates if the package name follows Android package naming conventions.

        Uses regex pattern based on Android conventions:
        - Must start with a letter (a-z, A-Z)
        - Can contain letters, digits, and underscores
        - Must have at least two segments separated by dots
        - Each segment must start with a letter
        - Pattern: ^[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z][a-zA-Z0-9_]*)+$

        [Arguments]
        - package_name: The package name to validate

        [Return Values]
        - Returns True if valid, False otherwise

        [Examples]
        Valid: com.example.app, com.google.android.youtube, my.app.test_2
        Invalid: com, 123.app, .com.app, com..app, com.123app
        """
        if not package_name or not isinstance(package_name, str):
            return False

        # Android package name regex pattern
        # ^[a-zA-Z][a-zA-Z0-9_]* - First segment: starts with letter, followed by letters/digits/underscores
        # (\.[a-zA-Z][a-zA-Z0-9_]*)+ - Additional segments: dot + letter + letters/digits/underscores (one or more)
        android_package_pattern = r'^[a-zA-Z][a-zA-Z0-9_-]*(\.[a-zA-Z][a-zA-Z0-9_-]*)+$'

        return bool(re.match(android_package_pattern, package_name))
