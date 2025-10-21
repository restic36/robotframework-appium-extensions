# Wait Multiple Elements — AppiumLibrary Extension

`WaitMultipleElements` is a custom keyword designed to wait for multiple elements simultaneously on mobile applications using Appium and Robot Framework. It provides flexible waiting strategies and returns detailed visibility status for each element.

---

## Purpose

- Wait for multiple UI elements to become visible with configurable strategies (ALL or ANY)
- Provide a device-agnostic solution that works across different Android applications
- Enable precise synchronization for complex UI scenarios when multiple elements load asynchronously
- Support testing of dynamic content loading and multi-element validation
- Validate element visibility states with detailed feedback for debugging
- Enable automation of complex flows requiring multiple element confirmation

---

## How It Works

The keyword continuously polls for element visibility using the provided locators and applies different waiting strategies:

| Strategy | Description |
|----------|-------------|
| `wait_for_all=True` | Waits until ALL elements are visible |
| `wait_for_all=False` | Waits until ANY element is visible |
| Polling interval | Configurable check frequency (default: 0.5s) |
| Timeout protection | Maximum wait time before failure |
| Result dictionary | Returns visibility status for each locator |

The keyword performs validation to ensure:
- Elements list is not empty
- Appium driver is available
- Timeout values are positive
- Locators follow proper format

---

## How To Execute

### Basic Usage

```robot
@{locators}=    Create List    id=button1    xpath=//android.widget.TextView[@text="Submit"]
${result}=    Wait Multiple Elements    ${locators}    timeout=15    wait_for_all=True
```

### Test Suite Execution

To execute all test cases:

```bash
robot test_wait_multiple_elements.robot
```

Make sure that:
- `AppiumLibrary` and the `WaitMultipleElements` keyword are correctly imported
- The emulator or physical device is connected and responsive
- The target application is launched and accessible

---

## Parameters

- `elements_list`: List of element locators - **Required**
- `timeout`: Maximum wait time in seconds - **Optional** (default: 10)  
- `wait_for_all`: Strategy flag (True=ALL, False=ANY) - **Optional** (default: True)
- `polling_interval`: Check frequency in seconds - **Optional** (default: 0.5)

---

## Examples

### Wait for all elements to be visible
```robot
@{locators}=    Create List
...    id=com.android.vending:id/search_box_idle_text
...    xpath=//android.widget.TextView[@text="Top charts"]
...    accessibility_id=navigation_menu

${result}=    Wait Multiple Elements    ${locators}    timeout=15    wait_for_all=True
Should Be True    ${result['id=com.android.vending:id/search_box_idle_text']}
```

### Wait for any element to appear
```robot
@{locators}=    Create List
...    xpath=//android.widget.TextView[@text="Loading..."]
...    xpath=//android.widget.TextView[@text="Error occurred"]

${result}=    Wait Multiple Elements    ${locators}    timeout=10    wait_for_all=False
```

### Complex Play Store scenario
```robot
@{complex_locators}=    Create List
...    xpath=//androidx.compose.ui.platform.ComposeView[@resource-id="com.android.vending:id/0_resource_name_obfuscated"]/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View[1]
...    xpath=//android.widget.TextView[@text="Find fellow bookworms with Facebook Events. Connect with readers who get it."]

${result}=    Wait Multiple Elements    ${complex_locators}    timeout=20    wait_for_all=True
```

### Rapid polling for dynamic content
```robot
@{dynamic_elements}=    Create List
...    id=loading_spinner
...    id=content_loaded

${result}=    Wait Multiple Elements    ${dynamic_elements}    timeout=30    wait_for_all=False    polling_interval=0.1
```

---

## Technical Details

- Built to work with AppiumLibrary and Robot Framework
- Uses AppiumLibrary's internal `_element_find()` method for element location
- Implements continuous polling mechanism with configurable intervals
- Supports all AppiumLibrary locator strategies (id, xpath, accessibility_id, etc.)
- Returns structured dictionary results for programmatic validation
- Provides comprehensive logging for debugging and monitoring

---

## Code Structure

- Implemented as a class (`WaitMultipleElements`) with `ROBOT_LIBRARY_SCOPE = GLOBAL`
- Modular architecture with comprehensive error handling
- Uses Robot Framework's BuiltIn library for logging and library access
- Designed for reliability, performance, and maintainability
- Thread-safe implementation for concurrent test execution

---

## Test Structure

The keyword has been validated through comprehensive test scenarios:

### Successful Wait Tests

- **Wait for all elements (Play Store)** - Complex XPath locators validation
- **Wait for any element (Play Store)** - Mixed existing/non-existing elements
- **Cross-application compatibility** - Tested across multiple Android apps
- **Boundary value testing** - Exact timeout and polling limits

### Timeout and Error Handling

- **No elements exist** - Proper timeout behavior validation
- **Partial element visibility** - Mixed visibility scenarios
- **Invalid locator handling** - Malformed locator syntax management
- **Driver availability** - Connection loss recovery testing

### Edge Cases

- **Empty element list** - Input validation testing
- **Rapid state changes** - UI transition reliability
- **Network-dependent elements** - Slow-loading content scenarios
- **Mixed locator strategies** - Combined id/xpath/accessibility_id usage

### Error Handling

The keyword provides clear error messages for:
- Empty elements list
- Timeout conditions (specific to ALL vs ANY strategy)
- Invalid locator syntax
- Driver availability issues
- Polling interval validation

---

## Use Cases

- **Form validation** - Wait for multiple input fields and buttons to appear
- **Loading screens** - Wait for either loading completion or error messages
- **Navigation flows** - Ensure all required navigation elements are present
- **Dynamic content** - Wait for multiple asynchronous elements to load
- **Cross-platform testing** - Reliable element waiting across different devices
- **Complex UI scenarios** - Handle multi-step processes with multiple validation points

---

## Return Format

The keyword returns a dictionary where:
- **Keys**: Original locator strings
- **Values**: Boolean visibility status (`True` if visible, `False` if not)

```python
{
    'id=button1': True,
    'xpath=//android.widget.TextView[@text="Submit"]': True,
    'accessibility_id=nonexistent': False
}
```

This format allows for detailed post-execution validation and debugging, enabling precise control over test flow based on individual element