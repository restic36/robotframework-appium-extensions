# Click Elements — AppiumLibrary Extension

`ClickElements` is a custom keyword designed to perform sequential clicks on multiple elements in mobile applications using Appium and Robot Framework. It provides precise control over click timing, duration, and intervals between clicks.

---

## Purpose

- Execute sequential clicks on multiple UI elements with configurable timing
- Provide a device-agnostic solution that works across different Android applications
- Enable automated interaction sequences for complex workflows and calculations
- Support testing of multi-step processes requiring sequential element interaction
- Validate click sequences with customizable delays and durations
- Enable automation of forms, calculators, and multi-button interactions

---

## How It Works

The keyword processes a list of element locators and performs sequential clicks with configurable parameters:

| Parameter | Description |
|-----------|-------------|
| `elements_list` | List of element locators to click sequentially |
| `click_duration` | Duration of each individual click in milliseconds |
| `interval_between_clicks` | Time delay between clicks in seconds |
| Element finding | Uses AppiumLibrary's `_element_find()` method |
| Center calculation | Automatically calculates element center coordinates |
| Touch simulation | Uses W3C WebDriver Actions API for precise clicks |

The keyword performs validation to ensure:
- Elements list is not empty and is a proper list
- Appium driver is available
- Click duration and intervals are positive values
- Elements can be found before clicking

---

## How To Execute

### Basic Usage

```robot
@{elements}=    Create List    id=button1    xpath=//android.widget.TextView[@text="Submit"]
Click Elements    ${elements}    click_duration=200    interval_between_clicks=0.5
```

### Test Suite Execution

To execute all test cases:

```bash
robot test_click_elements.robot
```

Make sure that:
- `AppiumLibrary` and the `ClickElements` keyword are correctly imported
- The emulator or physical device is connected and responsive
- The target application is launched and accessible

---

## Parameters

- `elements_list`: List of element locators - **Required**
- `click_duration`: Duration of each click in milliseconds - **Optional** (default: 100)  
- `interval_between_clicks`: Time between clicks in seconds - **Optional** (default: 0.5)

---

## Examples

### Click multiple calculator buttons using ID locators
```robot
@{elements}=    Create List
...    id=com.google.android.calculator:id/digit_1
...    id=com.google.android.calculator:id/digit_2
...    id=com.google.android.calculator:id/digit_3

Click Elements    ${elements}    click_duration=200    interval_between_clicks=0.5
```

### Click using XPath locators
```robot
@{elements}=    Create List
...    xpath=//android.widget.ImageButton[@content-desc="4"]
...    xpath=//android.widget.ImageButton[@content-desc="5"]
...    xpath=//android.widget.ImageButton[@content-desc="6"]

Click Elements    ${elements}    click_duration=250    interval_between_clicks=0.6
```

### Perform calculation using mixed locator types
```robot
# Calculate: 2 + 3 = using mixed locators
@{elements}=    Create List
...    id=com.google.android.calculator:id/digit_2
...    xpath=//android.widget.ImageButton[@content-desc="plus"]
...    accessibility_id=3
...    id=com.google.android.calculator:id/eq

Click Elements    ${elements}    click_duration=200    interval_between_clicks=0.5
```

### Fast sequential clicks
```robot
@{rapid_elements}=    Create List
...    id=button1    id=button2    id=button3

Click Elements    ${rapid_elements}    click_duration=50    interval_between_clicks=0.1
```

### Slow deliberate clicks
```robot
@{slow_elements}=    Create List
...    xpath=//android.widget.Button[@text="Start"]
...    xpath=//android.widget.Button[@text="Process"]
...    xpath=//android.widget.Button[@text="Finish"]

Click Elements    ${slow_elements}    click_duration=500    interval_between_clicks=2.0
```

---

## Technical Details

- Built to work with AppiumLibrary and Robot Framework
- Uses AppiumLibrary's internal `_element_find()` method for element location
- Implements W3C WebDriver Actions API for precise touch simulation
- Supports all AppiumLibrary locator strategies (id, xpath, accessibility_id, etc.)
- Automatically calculates element center coordinates for optimal clicking
- Provides comprehensive logging for debugging and monitoring

---

## Code Structure

- Implemented as a class (`ClickElements`) with `ROBOT_LIBRARY_SCOPE = GLOBAL`
- Modular architecture with comprehensive error handling
- Uses Robot Framework's BuiltIn library for logging and library access
- Designed for reliability, performance, and maintainability
- Thread-safe implementation for concurrent test execution

---

## Test Structure

The keyword has been validated through comprehensive test scenarios:

### Successful Click Tests

- **Calculator ID locators** - Sequential clicks on number buttons using ID
- **Calculator XPath locators** - Sequential clicks using XPath expressions
- **Calculator accessibility IDs** - Sequential clicks using accessibility identifiers
- **Mixed locator calculation** - Complex calculation using different locator types

### Timing and Performance Tests

- **Fast sequential clicks** - Rapid clicking with minimal delays
- **Slow deliberate clicks** - Extended delays for UI responsiveness
- **Variable durations** - Different click durations for various scenarios
- **Stress testing** - Multiple iterations with different timing configurations

### Error Handling

- **Empty elements list** - Validates proper error handling for empty input
- **Non-existent elements** - Handles missing elements gracefully with warnings
- **Invalid locators** - Manages malformed locator syntax
- **Driver availability** - Validates behavior when Appium connection is lost

### Edge Cases

- **Single element list** - Validates behavior with only one element
- **Large element lists** - Performance testing with many elements
- **Mixed element states** - Handling of visible/invisible elements
- **Rapid state changes** - Reliability during UI transitions

---

## Use Cases

- **Calculator operations** - Sequential number and operator input
- **Form filling** - Multiple field interactions in sequence
- **Navigation flows** - Multi-step navigation through applications
- **Game interactions** - Sequential button presses for gaming scenarios
- **Configuration wizards** - Step-by-step setup processes
- **Multi-button workflows** - Complex processes requiring multiple interactions

---

## Return Behavior

The keyword executes all clicks in the provided sequence and:
- Logs successful clicks at INFO level
- Logs warnings for elements that cannot be found
- Continues execution even if some elements are not found
- Provides detailed timing information for each click
- Raises RuntimeError only for critical failures (driver issues, invalid parameters)

This approach ensures maximum test reliability while providing clear feedback about any issues encountered during execution.