from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import subprocess
import time

class ChangeTheme:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()
        self.device_udid = None  

    @property
    def appium(self):
        return self._builtin.get_library_instance("AppiumLibrary")
    
    @keyword("Set Device UDID")
    def set_device_udid(self, udid):
        """Set the device UDID dynamically.

        Args:
            udid (str): The unique device identifier.
        """
        self.device_udid = udid
        self._builtin.log(f"UDID set to: {udid}", "INFO")

    def _execute_adb_command(self, command):
        """Execute an ADB command and return the result.

        Args:
            command (str): The ADB command to be executed.

        Returns:
            tuple: (success: bool, output: str) with command status and response.
        """
        try:
            full_command = f"adb -s {self.device_udid} {command}"
            result = subprocess.run(
                full_command.split(),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self._builtin.log(f"ADB command executed: {full_command}", "INFO")
                return True, result.stdout.strip()
            else:
                self._builtin.log(f"ADB command error: {result.stderr}", "ERROR")
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            self._builtin.log(f"ADB command timeout: {command}", "ERROR")
            return False, "Timeout"
        except Exception as e:
            self._builtin.log(f"Error executing ADB command: {str(e)}", "ERROR")
            return False, str(e)

    def _get_current_theme(self):
        """Retrieve the current system theme using `getprop` and `settings`.

        Returns:
            str | None: The current theme code (0=auto, 1=light, 2=dark), or None if unavailable.
        """
        success, output = self._execute_adb_command("shell settings get secure ui_night_mode")
        if success:
            return output.strip()
        return None

    def _set_theme_via_adb(self, mode):
        """Set the system theme using ADB commands.

        Args:
            mode (str): "dark" for dark theme, "light" for light theme.

        Raises:
            RuntimeError: If the theme could not be applied.

        Returns:
            bool: True if applied successfully.
        """
        cmd_value = "yes" if mode == "dark" else "no"
        command = f"shell cmd uimode night {cmd_value}"
        success, output = self._execute_adb_command(command)

        if not success:
            raise RuntimeError(f"Failed to set {mode} theme: {output}")

        self._builtin.log(f"{mode.capitalize()} theme applied via 'cmd uimode'", "INFO")
        time.sleep(1)
        return True

    def _verify_theme_change(self, expected_mode):
        """Verify if the theme has been changed correctly.

        Args:
            expected_mode (str): Expected theme, "dark" or "light".

        Returns:
            bool: True if verification passed, False otherwise.
        """
        expected_values = {
            "dark": "2",
            "light": "1"
        }
        
        current_theme = self._get_current_theme()
        if current_theme == expected_values[expected_mode]:
            self._builtin.log(f"{expected_mode.capitalize()} theme successfully applied (code: {current_theme})", "INFO")
            return True
        else:
            self._builtin.log(f"Theme not applied. Expected: {expected_values[expected_mode]}, Current: {current_theme}", "WARN")
            return False

    @keyword("Change To Dark Theme")
    def change_to_dark_theme(self, verify=True):
        """Switch system to dark theme using ADB.

        Args:
            verify (bool, optional): If True, verifies that the change was applied. Defaults to True.

        Raises:
            RuntimeError: If theme change fails.

        Returns:
            bool: True if the theme was set successfully.
        """
        try:
            self._builtin.log("Starting dark theme switch via ADB", "INFO")
            
            current_theme = self._get_current_theme()
            self._builtin.log(f"Current theme: {current_theme}", "INFO")
            
            if current_theme == "2":
                self._builtin.log("Device is already using dark theme", "INFO")
                return True
            
            self._set_theme_via_adb("dark")
            
            if verify:
                if not self._verify_theme_change("dark"):
                    raise RuntimeError("Dark theme was not applied correctly")
            
            self._builtin.log("Dark theme successfully applied", "INFO")
            return True
            
        except Exception as e:
            self._builtin.log(f"Error switching to dark theme: {str(e)}", "ERROR")
            raise RuntimeError(f"Failed to switch to dark theme: {str(e)}")

    @keyword("Change To Light Theme")
    def change_to_light_theme(self, verify=True):
        """Switch system to light theme using ADB.

        Args:
            verify (bool, optional): If True, verifies that the change was applied. Defaults to True.

        Raises:
            RuntimeError: If theme change fails.

        Returns:
            bool: True if the theme was set successfully.
        """
        try:
            self._builtin.log("Starting light theme switch via ADB", "INFO")
            
            current_theme = self._get_current_theme()
            self._builtin.log(f"Current theme: {current_theme}", "INFO")
            
            if current_theme == "1":
                self._builtin.log("Device is already using light theme", "INFO")
                return True
            
            self._set_theme_via_adb("light")
            
            if verify:
                if not self._verify_theme_change("light"):
                    raise RuntimeError("Light theme was not applied correctly")
            
            self._builtin.log("Light theme successfully applied", "INFO")
            return True
            
        except Exception as e:
            self._builtin.log(f"Error switching to light theme: {str(e)}", "ERROR")
            raise RuntimeError(f"Failed to switch to light theme: {str(e)}")

    @keyword("Get Current Theme")
    def get_current_theme(self):
        """Get the current system theme.

        Returns:
            str: "auto", "light", "dark", or "unknown".
        """
        try:
            theme_code = self._get_current_theme()
            theme_map = {
                "0": "auto",
                "1": "light", 
                "2": "dark"
            }
            
            theme_name = theme_map.get(theme_code, "unknown")
            self._builtin.log(f"Current theme: {theme_name} (code: {theme_code})", "INFO")
            return theme_name
            
        except Exception as e:
            self._builtin.log(f"Error getting current theme: {str(e)}", "ERROR")
            raise RuntimeError(f"Failed to get current theme: {str(e)}")

    @keyword("Toggle Theme")
    def toggle_theme(self):
        """Toggle between light and dark themes.
        
        If current theme is auto, defaults to dark.
        """
        try:
            current_theme = self.get_current_theme()
            
            if current_theme == "dark":
                self.change_to_light_theme()
            elif current_theme == "light":
                self.change_to_dark_theme()
            else:
                self.change_to_dark_theme()
                
            self._builtin.log("Theme successfully toggled", "INFO")
            return True
            
        except Exception as e:
            self._builtin.log(f"Error toggling theme: {str(e)}", "ERROR")
            raise RuntimeError(f"Failed to toggle theme: {str(e)}")

    @keyword("Reset Theme To Auto")
    def reset_theme_to_auto(self):
        """Reset the system theme to automatic mode.

        Raises:
            RuntimeError: If reset fails.

        Returns:
            bool: True if reset successfully.
        """
        try:
            self._builtin.log("Resetting theme to auto mode", "INFO")

            command = "shell settings put secure ui_night_mode 0"
            success, output = self._execute_adb_command(command)

            if not success:
                raise RuntimeError(f"Failed to reset theme: {output}")

            self._builtin.log("Theme reset to auto successfully", "INFO")
            return True

        except Exception as e:
            self._builtin.log(f"Error resetting theme: {str(e)}", "ERROR")
            raise RuntimeError(f"Failed to reset theme: {str(e)}")
