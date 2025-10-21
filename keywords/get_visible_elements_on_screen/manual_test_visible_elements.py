from VisibleElements import VisibleElements
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import json

# Create a fake BuiltIn to simulate .log() and .fail()
class FakeBuiltIn:
    def log(self, msg, level=None):
        print(f"[{level}] {msg}")
    def fail(self, msg):
        raise Exception(msg)
    
# Mocked version of VisibleElements to inject the driver directly
class MockVisibleElements(VisibleElements):
    def __init__(self, mock_driver):
        self._driver = mock_driver
        self._builtin = FakeBuiltIn()

    def _get_appium_driver(self):
        return self._driver


# Basic element mock to simulate screen elements
class Element:
    def __init__(self, displayed, rid, text="", cls="", clickable="false", raise_display=False):
        self.text = text
        self.attrs = {
            "resource-id": rid,
            "content-desc": None,
            "class": cls,
            "clickable": clickable
        }
        self.raise_display = raise_display
        self._displayed = displayed

    def is_displayed(self):
        if self.raise_display:
            raise StaleElementReferenceException("Simulated stale element")
        return self._displayed

    def get_attribute(self, name):
        if name not in self.attrs:
            raise NoSuchElementException(f"Attribute '{name}' not found")
        return self.attrs[name]


# Fake Appium driver mock
class MockDriver:
    def __init__(self, elements):
        self.elements = elements

    def find_elements(self, by, locator):
        return self.elements


# === MANUAL TEST EXECUTION ===
if __name__ == "__main__":
    print("=== Manual tests: Get Visible Elements On Screen ===\n")

    cases = [
        #VISIBILITY case
        {
            "desc": "Visible element with resource_id",
            "elements": [Element(True, "btn_login", text="Login", cls="android.widget.Button", clickable="true")],
            "filter_type": "all",
            "debug": False,
            "expected": ["btn_login"]
        },
        #(IN)VISIBILITY case
        {
            "desc": "Invisible element with resource_id",
            "elements": [Element(False, "btn_cancel")],
            "filter_type": "all",
            "debug": False,
            "expected": []
        },
        # FILTERED BY TYPE case
        {
            "desc": "Filter by button class",
            "elements": [
                Element(True, "btn_ok", cls="android.widget.Button", clickable="true"),
                Element(True, "txt_header", cls="android.widget.TextView")
            ],
            "filter_type": "button",
            "debug": False,
            "expected": ["btn_ok"]
        },
        # DEBUG MODE case
        {
            "desc": "Input elements with debug mode",
            "elements": [
                Element(True, "inp_email", cls="android.widget.EditText"),
                Element(True, "inp_senha", cls="android.widget.EditText")
            ],
            "filter_type": "input",
            "debug": True,
            "expected": [
                {"resource_id": "inp_email", "accessibility_id": "null", "text": "", "class": "android.widget.EditText", "clickable": False},
                {"resource_id": "inp_senha", "accessibility_id": "null", "text": "", "class": "android.widget.EditText", "clickable": False},
            ]
        },
        # EXCEPTION case
        {
            "desc": "Element that raises exception (Stale)",
            "elements": [
                Element(True, "btn1"),
                Element(True, "btn2", raise_display=True), # Simulate stale element
                Element(True, "btn3")
            ],
            "filter_type": "all",
            "debug": False,
            "expected": ["btn1", "btn3"]
        },
    ]

    for case in cases:
        print(f"--- Test: {case['desc']} ---")
        driver = MockDriver(case["elements"])
        visible = VisibleElements()
        visible = MockVisibleElements(driver)

        result = visible.get_visible_elements_on_screen(filter_type=case["filter_type"], debug=case["debug"])
        print("✅ PASSED\n" if result == case["expected"] else "❌ FAILED\n")