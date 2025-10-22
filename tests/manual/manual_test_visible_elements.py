from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from VisibleElements import VisibleElements


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
    def __init__(self, displayed, rid, text="", cls="", clickable="false", raise_display=False, content_desc=None):
        self.text = text
        self.attrs = {
            "resource-id": rid,
            "content-desc": content_desc,
            "class": cls,
            "clickable": clickable,
            "text": text,
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
        # DETERMINISM CASE — trigger StaleElementReferenceException on a specific item
        {
            "desc": "Stale element is ignored deterministically (middle item)",
            "elements": [
                Element(True, "btn1", text="One", cls="android.widget.Button", clickable="true"),
                Element(True, "btn2", text="Two", cls="android.widget.Button", clickable="true", raise_display=True),
                Element(True, "btn3", text="Three", cls="android.widget.Button", clickable="true"),
            ],
            "filter_type": "all",
            "debug": False,
            "expected": ["btn1", "btn3"],
        },
        # NORMALIZATION CASE 1 — content-desc '  null  ' becomes '' (keep resource-id to ensure inclusion)
        {
            "desc": "Normalization: content-desc '  null  ' -> '' (debug payload)",
            "elements": [
                Element(
                    True,
                    "inp_name",
                    text="   ",
                    cls="android.widget.EditText",
                    clickable="false",
                    content_desc="  null  ",
                ),
            ],
            "filter_type": "input",
            "debug": True,
            "expected": [
                {
                    "identifier": {"value": "inp_name", "kind": "resource_id"},
                    "resource_id": "inp_name",
                    "accessibility_id": "",  # normalized from '  null  '
                    "text": "",  # normalized blank text
                    "class": "android.widget.EditText",
                    "clickable": False,
                }
            ],
        },
        # NORMALIZATION CASE 2 — missing content-desc (None) normalizes to ""
        {
            "desc": "Normalization: content-desc None -> '' (debug payload)",
            "elements": [
                Element(
                    True, "inp_email", text="", cls="android.widget.EditText", clickable="false", content_desc=None
                ),
            ],
            "filter_type": "input",
            "debug": True,
            "expected": [
                {
                    "identifier": {"value": "inp_email", "kind": "resource_id"},
                    "resource_id": "inp_email",
                    "accessibility_id": "",  # None -> ""
                    "text": "",
                    "class": "android.widget.EditText",
                    "clickable": False,
                }
            ],
        },
        # IDENTIFIER CASE — auto prioritizes resource-id when both exist
        {
            "desc": "Identifier: auto prefers resource-id over content-desc (debug)",
            "elements": [
                Element(
                    True,
                    "btn_dual",
                    text="OK",
                    cls="android.widget.Button",
                    clickable="true",
                    content_desc="btn_dual_cd",
                ),
            ],
            "filter_type": "all",
            "debug": True,
            "expected": [
                {
                    "identifier": {"value": "btn_dual", "kind": "resource_id"},
                    "resource_id": "btn_dual",
                    "accessibility_id": "btn_dual_cd",
                    "text": "OK",
                    "class": "android.widget.Button",
                    "clickable": True,  # because we pass clickable="true"
                }
            ],
        },
        # DEDUP CASE — same (kind, value) for resource-id -> 1 item
        {
            "desc": "Dedup: same (kind,value) for resource-id collapses to one",
            "elements": [
                Element(True, "btn_dup", cls="android.widget.Button", clickable="true"),
                Element(True, "btn_dup", cls="android.widget.Button", clickable="true"),
            ],
            "filter_type": "all",
            "debug": False,
            "expected": ["btn_dup"],
        },
        # DEDUP CASE — same value across different kinds results in 2 entries (normal output is strings)
        {
            "desc": "Dedup: same value across different kinds (rid vs accessibility_id) keeps both",
            "elements": [
                Element(True, "btn_same", text="OK", cls="android.widget.Button", clickable="true"),
                Element(True, None, text="OK", cls="android.widget.Button", clickable="true", content_desc="btn_same"),
            ],
            "filter_type": "all",
            "debug": False,
            "expected": ["btn_same", "btn_same"],  # two items because (kind, value) differs
        },
        # LEGIT EMPTY CASE 1 — input with NO identifiers -> []
        {
            "desc": "Legit empty: input element without identifiers returns []",
            "elements": [
                Element(True, None, text="", cls="android.widget.EditText", clickable="false", content_desc=None),
            ],
            "filter_type": "input",
            "debug": False,
            "expected": [],
        },
        # LEGIT EMPTY CASE 2 (selector-strict) — require accessibility_id when only resource-id exists
        {
            "desc": "Legit empty (strict): id_mode=accessibility_id but element has only resource-id",
            "elements": [
                Element(
                    True, "input_user", text="", cls="android.widget.EditText", clickable="true", content_desc=None
                ),
            ],
            "filter_type": "input",
            "id_mode": "accessibility_id",
            "debug": False,
            "expected": [],
        },
        # CONTROL CASE 3 (selector-strict) — require accessibility_id and element has only content-desc
        {
            "desc": "Strict selector returns value when content-desc exists",
            "elements": [
                Element(
                    True, None, text="", cls="android.widget.EditText", clickable="true", content_desc="field_user"
                ),
            ],
            "filter_type": "input",
            "id_mode": "accessibility_id",
            "debug": False,
            "expected": ["field_user"],
        },
    ]

    for case in cases:
        print(f"--- Test: {case['desc']} ---")
        driver = MockDriver(case["elements"])
        visible = VisibleElements()
        visible = MockVisibleElements(driver)

        id_mode = case.get("id_mode", "auto")
        result = visible.get_visible_elements_on_screen(
            filter_type=case["filter_type"], id_mode=id_mode, debug=case["debug"]
        )
        print("✅ PASSED\n" if result == case["expected"] else "❌ FAILED\n")
