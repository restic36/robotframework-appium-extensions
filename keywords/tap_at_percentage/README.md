# Keyword Tap At Percentage — AppiumLibrary Extension

`TapAtPercentage` is a custom keyword designed to simplify and standardize screen tapping functionality in Android devices during tests using Appium and Robot Framework. It uses percentage-based coordinates to tap at specific points on the screen, making tests more reliable across different screen sizes.

---

## Purpose

- Tap at specific points on the screen using percentage coordinates (0.0 to 1.0)
- Provide a device-agnostic solution that works across different screen sizes
- Enable precise interaction with UI elements when traditional locators are not available
- Support testing of gesture-based interactions and coordinate-dependent features
- Validate touch interactions in custom UI components
- Enable automation of drawing, gaming, or map-based applications

---

## How It Works

The keyword converts percentage coordinates to absolute pixel coordinates based on the device's screen size:

| Coordinate | Description |
|------------|-------------|
| (0.0, 0.0) | Top-left corner |
| (0.5, 0.5) | Center of screen |
| (1.0, 1.0) | Bottom-right corner |
| (0.0, 1.0) | Bottom-left corner |
| (1.0, 0.0) | Top-right corner |

The keyword performs validation to ensure:
- Coordinates are between 0.0 and 1.0
- Duration is a positive integer
- Input values are numeric

---

## How To Execute

### Basic Usage

```robot
Tap At Percentage    x=0.5    y=0.5    duration=200
```

### Test Suite Execution

To execute all test cases:

```bash
robot test_tap_at_percentage.robot
```

Make sure that:
- `AppiumLibrary` and the `TapAtPercentage` keyword are correctly imported
- The emulator or physical device is connected and responsive
- The application under test is launched

---

## Parameters

- `x`: X coordinate as percentage (0.0 to 1.0) - **Required**
- `y`: Y coordinate as percentage (0.0 to 1.0) - **Required**  
- `duration`: Duration of the tap in milliseconds - **Optional** (default: 100)

---

## Examples

### Tap at screen center
```robot
Tap At Percentage    x=0.5    y=0.5    duration=200
```

### Tap at top-left corner
```robot
Tap At Percentage    x=0.0    y=0.0    duration=100
```

### Tap at bottom-right corner
```robot
Tap At Percentage    x=1.0    y=1.0    duration=150
```

### Rapid taps for gaming scenarios
```robot
FOR    ${i}    IN RANGE    5
    Tap At Percentage    x=0.5    y=0.5    duration=50
    Sleep    0.2s
END
```

---

## Technical Details

- Built to work with AppiumLibrary and Robot Framework
- Uses Selenium's ActionChains with W3C touch pointer actions
- Automatically converts percentage coordinates to pixel coordinates
- Designed for cross-device compatibility and maintainability
- Returns `True` on successful execution

---

## Code Structure

- Implemented as a class (`TapAtPercentage`) with `ROBOT_LIBRARY_SCOPE = GLOBAL`
- Modular architecture with comprehensive input validation
- Uses W3C WebDriver Actions API for precise touch simulation
- Leverages Appium's screen size detection for coordinate conversion

---

## Test Structure

The keyword has been validated through comprehensive test scenarios:

### Successful Tap Tests

- **Center tap** - Coordinates: (0.5, 0.5)
- **Corner taps** - All four corners of the screen
- **Calculator interactions** - Taping number buttons and operators
- **Boundary values** - Testing exact 0.0 and 1.0 coordinates
- **Decimal coordinates** - Testing precise fractional coordinates
- **Multiple rapid taps** - Performance and reliability testing

### Validation Tests

- **Invalid coordinates** - Values outside 0.0-1.0 range
- **Non-numeric inputs** - String values for coordinates
- **Invalid duration** - Negative, zero, or non-integer values
- **Edge cases** - Boundary condition testing

### Error Handling

The keyword provides clear error messages for:
- Coordinates outside valid range (0.0 to 1.0)
- Non-numeric coordinate values
- Invalid duration values
- Driver availability issues

---

## Use Cases

- **Gaming applications** - Precise touch interactions
- **Map applications** - Tapping specific geographic points
- **Drawing/sketching apps** - Coordinate-based drawing
- **Custom UI components** - When standard locators fail
- **Gesture testing** - Starting point for swipe gestures
- **Screen calibration** - Testing touch accuracy across devices