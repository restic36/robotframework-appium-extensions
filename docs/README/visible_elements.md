# Get Visible Elements On Screen — AppiumLibrary Extension

`VisibleElements` is a custom keyword to retrieve visible UI elements from the screen, with optional type filtering, identifier selection (`resource_id`, `content-desc`) and optional debug mode. Designed for mobile test automation with Robot Framework.

**Element Filtering Flow**
All screen elements
       ↓
is_displayed() == True?
       ↓
Passes filter type? (e.g., clickable, text)
       ↓
Yields a chosen identifier according to id_mode? (resource-id → fallback to content-desc in auto)
       ↓
Not a duplicate? (dedupe by (kind, value))
       ↓
→ Add to result

**Note:** On Android,  `accessibility_id` is an alias of `content-desc`.
The result in `auto` mode is a mixed list of identifiers (some `resource-id`, some `content-desc`).

---

## Purpose

Provide a reliable method to capture **visible and valid UI elements** during Appium-based mobile testing,broadening coverage beyond `resource-id`-only by supporting `content-desc` (accessibility) as a fallback or as the primary mode, while keeping the interface simple.

---

## How It Works

The keyword works by:
1. Capturing **all UI elements** from the screen using a generic XPath (`//*`);
2. Filtering out:
   - Elements that are **not visible** (`is_displayed() == False`);
   - Elements **that do not match the selected filter** (`clickable`, `text`, etc.);
   - Elements **without a usable identifier according to `id_mode`**:
       - `auto` → try `resource-id`, else fallback to `content-desc`;
       - `resource_id` → only `resource-id`;
       - `accessibility_id` → only `content-desc`;
   - Duplicates, using a set on `(kind, value)` (e.g., `("resource_id","com.app:id/login")`);
3. Returning a list of:
   - Identifier strings (`resource-id` or `content-desc`, depending on selection); or
   - Or structured dictionaries (debug mode) including both the selected identifier and raw attributes for inspection.

---

## How To Use

In a Robot Framework test case:

```robot
*** Settings ***
Library    VisibleElements.py

*** Test Cases ***
Return Clickable Elements
    ${result}=    Get Visible Elements On Screen    clickable  auto
    Log    ${result}

Return Text Fields in Debug Mode
    ${result}=    Get Visible Elements On Screen    text   auto    debug=True
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

| Argument      | Type | Default | Description                                                                                          |
|---------------|------|---------|------------------------------------------------------------------------------------------------------|
| `filter_type` | str  | all     | Filter applied to elements. Options: `all`, `clickable`, `text`, `button`, `input`.                  |
| `id_mode`     | str  | auto    | Identifier mode. Options: `auto`, `resorce_id`, `accessibility_id` (Android alias of `content-desc`) |
| `debug`       | bool | False   | If True, returns detailed element info in JSON format; otherwise, just IDs.                          |

- In `auto`, the keyword prefers `resource-id`, and falls back to `content-desc` if the former is empty—expanding coverage with a single, simple option.

---

## Internal Validations

- Considers only elements with `is_displayed() == True`
- Chooses an identifier per `id_mode`:
       - `auto`: `resource-id` → fallback to `content-desc`
       - `resource_id`: requires non-empty `resource-id`
       - `accessibility_id`: requires non-empty `content-desc`
- Applies the appropriate logic for each filter type
- Deduplicates by tuple `(kind, value)` to avoid cross-type collisions
- Skips invalid DOM references (`StaleElementReferenceException`, `NoSuchElementException`)
- Provides informative logging: number of elements discovered and returned; pretty-printed JSON when debug=True
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

- **Type filtering:** returns only visible elements matching filter_type (`all`, `button`, `input`, `clickable`, `text`)
- **Identifier selection:** `auto` prefers `resource-id` over `content-desc`; explicit modes (`resource_id`, `accessibility_id`) validated; dedup by (kind, value)
- **Strict-empty semantics:** restrictive combos may legitimately return an empty list (suite must not fail)
- **Debug payload:** items follow the stable schema and fields are normalized
- **Error handling:** invisible/missing-identifier nodes are excluded; invalid args fail fast with clear messages.

### Mocked Tests

In addition to automated test cases, mocked test cases were created to validate the core logic of the VisibleElements keyword and to
covering edge cases that are hard to reproduce reliably on real screens:

- **Visibility & stale:** only elements that pass `is_displayed()` are considered; targeted `StaleElementReferenceException` is ignored
- **Identifier selection:** `id_mode=auto` prefers `resource-id` over `content-desc`
- **Normalization rules:** whitespace/`"null"`/`None` → `""`; `clickable` normalized; missing/exception-throwing attributes handled safely
- **Type filtering:** respects filter_type (`button`, `input`, `clickable`, `text`, `all`)
- **Strict-empty & dedup:** empty lists are valid for restrictive combos; de-dup by `(kind, value)` — same value across different kinds is kept twice
- **Stable debug schema:** with `debug=True`, each item is
`{"identifier": {"value","kind"}, "resource_id", "accessibility_id", "text", "class", "clickable"}` (all fields normalized)
 
---

##  Known limitations and errors

- Elements lacking **both** `resource-id` **and** `content-desc` are ignored (no usable identifier)
- Elements from hybrid/native-web views may not be captured
- Invalid `filter_type` raises a `BuiltIn.fail()` error with accepted options
- If screen transitions or animations occur during element lookup, stale elements may be more frequent
- Designed primarily for Android; iOS may require mapping to equivalent attributes (e.g., `name`/`label`)
- The result list in `auto` is mixed: some entries are `resource-id`, others are `content-desc`