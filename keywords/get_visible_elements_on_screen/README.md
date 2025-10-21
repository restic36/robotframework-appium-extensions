# Get Visible Elements On Screen — AppiumLibrary Extension

`VisibleElements` is a custom keyword to retrieve visible UI elements from the screen, with filtering options by type and optional debug mode. Designed for mobile test automation with Robot Framework.

**Element Filtering Flow**
All screen elements
       ↓
is_displayed() == True?
       ↓
Has valid resource-id?
       ↓
Passes filter type? (e.g., clickable, text)
       ↓
→ Add to result

---

## Purpose

Provide a reliable method to capture **visible and valid UI elements** during Appium-based mobile testing, filtering results based on common element types and excluding non-visible or invalid references.

---

## How It Works

The keyword works by:
1. Capturing **all UI elements** from the screen using a generic XPath (`//*`);
2. Filtering out:
   - Elements that are **not visible** (`is_displayed() == False`);
   - Elements **without a valid `resource-id`**;
   - Elements **that do not match the selected filter** (`clickable`, `text`, etc.);
3. Returning a list of:
   - `resource-id` strings (default mode);
   - Or structured dictionaries (debug mode).

---

## How To Use

In a Robot Framework test case:

```robot
*** Settings ***
Library    VisibleElements.py

*** Test Cases ***
Return Clickable Elements
    ${result}=    Get Visible Elements On Screen    clickable
    Log    ${result}

Return Text Fields in Debug Mode
    ${result}=    Get Visible Elements On Screen    text    debug=True
    Log    ${result}
```

---

## How To Execute

To run the tests:

```bash
robot VisibleElements.robot
```

Make sure that:
- Appium is running
- The emulator/device is online
- `AppiumLibrary` and the `VisibleElements` keyword are correctly imported

---

## Arguments

| Argument      | Type | Default | Description                                                                         |
|---------------|------|---------|-------------------------------------------------------------------------------------|
| `filter_type` | str  | all     | Filter applied to elements. Options: `all`, `clickable`, `text`, `button`, `input`. |
| `debug`       | bool | False   | If True, returns detailed element info in JSON format; otherwise, just IDs.         |

---

## Internal Validations

- Filters only elements with `is_displayed() == True`
- Requires `resource-id` to be present and non-null
- Applies the appropriate logic for each filter type
- Skips invalid DOM references (`StaleElementReferenceException`, `NoSuchElementException`)
- Logs total number of elements found and returned

---

## Technical Details

- Built to work with AppiumLibrary and Robot Framework
- Uses `AppiumLibrary` as driver interface
- Returns structured output using `json.dumps()` for logging
- Designed for simplicity, reliability, and maintainability

## Code Structure

- Written as a class (VisibleElements) with ROBOT_LIBRARY_SCOPE = GLOBAL
- Modularized with helper functions (`find_all_elements`, `passes_filter` etc.)
- Includes explicit filtering and informative logging
- Designed for clarity, testability, and reuse

---

## Test Structure

The keyword has been validated through:

- **Basic filter validation:** Ensures correct filtering by type
- **Debug structure validation:** Checks dictionary keys for debug output
- **Error handling:** Verifies behavior when invalid filters are passed
- **Edge case handling:** Ensures ignored elements (e.g., no resource-id, blank text, invisible elements) are not returned

### Mocked Tests

In addition to automated test cases, mocked test cases were created to validate the core logic of the VisibleElements keyword:

- **Resource-id enforcement:** Ensures that only elements with valid, non-null `resource-id`s are returned
- **Basic visibility filter:** Validates that only visible elements are considered
- **Edge case rejection:** Confirms that invisible elements or those missing required attributes are not included in the result
- **Type-based filtering:** Confirms that elements are returned according to the selected `filter_type` (e.g., `button`, `input`)
- **Debug output validation:** Verifies that the debug mode returns detailed dictionaries with expected attributes
- **Exception handling:** Validates that `StaleElementReferenceException` are gracefully handled and logged

---

##  Known limitations and errors

- Elements without `resource-id` are ignored
- Elements from hybrid/native-web views may not be captured
- Invalid `filter_type` raises a `BuiltIn.fail()` error with accepted options
- If screen transitions or animations occur during element lookup, stale elements may be more frequent
- Designed primarily for Android; may need adaptation for iOS