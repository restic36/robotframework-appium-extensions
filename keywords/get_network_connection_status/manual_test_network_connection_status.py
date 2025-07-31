from NetworkStatus import NetworkStatus

# Mock for the Appium driver
class MockDriver:
    def __init__(self, network_status):
        self.network_connection = network_status

# Mock for the AppiumLibrary
class MockAppiumLibrary:
    def __init__(self, network_status):
        self.driver = MockDriver(network_status)

    def _current_application(self):
        return self.driver

# Mock for Robot Framework's BuiltIn library
class MockBuiltIn:
    def get_library_instance(self, name):
        return self.mock_appium

    def log(self, message, level):
        print(f"[{level}] {message}")

# Generic mock for subprocess.run
def create_mock_subprocess(airplane_mode_enabled):
    def mock_subprocess_run(args, capture_output=True, text=True, timeout=2, stdout=None, stderr=None):
        class Result:
            def __init__(self, stdout_text):
                self.stdout = stdout_text

        if 'airplane_mode_on' in args:
            return Result('1\n' if airplane_mode_enabled else '0\n')
        
        return Result('')

    return mock_subprocess_run


# === EXECUTION ===
if __name__ == "__main__":
    import subprocess

    # List of test cases with bitmask and airplane mode status
    test_cases = [
        {"bitmask": 0, "desc": "No network (NONE)", "airplane_mode": False},
        {"bitmask": 1, "desc": "Airplane mode enabled (AIRPLANE_MODE)", "airplane_mode": True},
        {"bitmask": 2, "desc": "Wi-Fi only", "airplane_mode": False},
        {"bitmask": 4, "desc": "Mobile data only", "airplane_mode": False},
        {"bitmask": 6, "desc": "Wi-Fi and mobile data", "airplane_mode": False},
        {"bitmask": 8, "desc": "Unknown bitmask (UNKNOWN)", "airplane_mode": False},
    ]

    for case in test_cases:
        print(f"\n--- Test: {case['desc']} ---")

        # Override subprocess.run with a custom mock
        subprocess.run = create_mock_subprocess(case["airplane_mode"])

        # Instantiate the mock BuiltIn and AppiumLibrary
        builtin = MockBuiltIn()
        builtin.mock_appium = MockAppiumLibrary(case["bitmask"])

        # Instantiate the keyword and inject the mocked BuiltIn
        net = NetworkStatus()
        net._builtin = builtin

        status = net.get_readable_network_status()
        print(f"Returned network status: {status}")