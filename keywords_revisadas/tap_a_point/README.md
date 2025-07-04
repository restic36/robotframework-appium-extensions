# Perform Tap A Point — AppiumLibrary Extension

`Tap A Point` is a custom keyword for the Robot Framework AppiumLibrary. It performs a precise tap gesture on a specific screen coordinate using W3C-compliant touch actions.

---

## Purpose

Provide a flexible and low-level alternative to tap anywhere on the screen using absolute coordinates. Useful when:

- Tapping specific screen points that don't belong to a single UI element
- Performing long-press interactions at fixed positions
- Customizing touch gesture duration

---

## How It Works

Internally, this keyword uses:

- `ActionChains` with W3C Touch API from Selenium
- A virtual “finger” pointer for realistic input simulation
- Absolute coordinates defined by the user
- Duration control (press and hold)

---

## How to Execute

To run the tests:

```bash
robot tap_a_point.robot
```

Make sure that:
- Appium is running
- The emulator/device is online

---

## Arguments

| Argument   | Type  | Default | Description                                   |
|------------|-------|---------|-----------------------------------------------|
| `x`        | int   | –       | X-coordinate of the screen                    |
| `y`        | int   | –       | Y-coordinate of the screen                    |
| `duration` | int   | 100     | Touch press duration (in milliseconds)        |

---

## Internal Validations

- Ensures `x` and `y` are valid integers
- Ensures `duration` is a positive integer
- Adjusts coordinates to fit within screen boundaries
- Logs a warning if coordinates were modified

---

## Technical Details

- Uses `ActionChains` and `W3C Actions`
- Compatible with AppiumLibrary for Robot Framework
- Emulates a realistic human touch gesture using virtual pointer
- Logs actions using `BuiltIn().log` for better traceability

---

## Code Structure

- Written as a class (TapAPoint) with ROBOT_LIBRARY_SCOPE = GLOBAL
- Modularized with helper functions (`get_driver`, `adjust_coordinates_to_screen_bounds`, etc.)
- Includes explicit argument validation and informative logging
- Designed for clarity, testability, and reuse

---

## Additional Notes

This keyword was originally created to fill a gap in AppiumLibrary's touch support and remains a valuable technical reference.

For native alternatives with multi-touch support, see the Tap With Positions README.