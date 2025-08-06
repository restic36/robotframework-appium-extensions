from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import subprocess

class NetworkStatus:
    """
    Keyword that interprets the connection bitmask returned by Appium and identifies the network status of the Android device.
    Also considers airplane mode via ADB.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()

    def _get_appium_driver(self):
    # Gets the current Appium driver instance
        appium_lib = self._builtin.get_library_instance("AppiumLibrary")
        return appium_lib._current_application()
    
    def _interpret_bitmask(self, status):
    # Bitwise AND is used to compare the bitmask and identify which connections are active.
    # Interprets the meaning behind the combined bits and returns: wifi, data, no_network
        wifi = (status & 2) != 0
        data = (status & 4) != 0
        no_network = status == 0
        return wifi, data, no_network
    
    def _airplane_mode_enabled(self):
    # Returns True if airplane mode is enabled via ADB settings, False otherwise.
        try:
            result = subprocess.run(
                ['adb', 'shell', 'settings', 'get', 'global', 'airplane_mode_on'],
                capture_output=True,
                text=True,
                timeout=2
            )
            return result.stdout.strip() == '1'
        except Exception as e:
            self._builtin.log(f"Error checking airplane mode: {e}", level='WARN')
            return False
        
    def _get_network_status(self, wifi, data, airplane_mode, no_network):
    # Returns a readable string representing the final network status, based on the bitmask and airplane mode
        if airplane_mode:
            return 'AIRPLANE_MODE'
        # In case where no bits are active (Wi-Fi, data, and airplane mode are off)
        elif no_network: 
            return 'NONE'
        elif wifi and data:
            return 'WIFI_AND_DATA'
        elif wifi:
            return 'WIFI_ONLY'           
        elif data:
            return 'DATA_ONLY'
        # Fallback case: if none of the above conditions match (this shouldn't occur under normal conditions)
        # Handles possible anomalies in the bitmask or unexpected status values
        else: 
            return 'UNKNOWN'

    @keyword('Get Readable Network Status')
    def get_readable_network_status(self):
        """
        Coordinates the full process by combining all internal steps
        and returns a readable string representing the current network connection type.

        Uses:
        - `driver.network_connection` to check Wi-Fi and mobile data bits
        - `adb shell settings get global airplane_mode_on` to detect airplane mode

        Possible return values:
        - WIFI_AND_DATA
        - WIFI_ONLY
        - DATA_ONLY
        - AIRPLANE_MODE
        - NONE
        - UNKNOWN
        """

        # Retrieves the network status as an integer (bitmask)
        driver = self._get_appium_driver()
        status = driver.network_connection 

        # Logs the read bitmask and its binary representation for debugging
        self._builtin.log(f"Read bitmask: {status} (binary: {bin(status)})", level='INFO')

        wifi, data, no_network = self._interpret_bitmask(status)
        airplane_mode = self._airplane_mode_enabled()

        # Logs the interpreted bits (whether each network type is active using True or False)
        self._builtin.log(f"Wi-Fi enabled: {wifi}", level='INFO')
        self._builtin.log(f"Mobile data enabled: {data}", level='INFO')
        self._builtin.log(f"Airplane mode: {airplane_mode}", level='INFO')
        self._builtin.log(f"No network active: {no_network}", level='INFO')

        # Determines the final network status based on the interpreted bits
        final_status = self._get_network_status(wifi, data, airplane_mode, no_network)
        self._builtin.log(f"Final interpreted status: {final_status}", level='INFO')

        return final_status