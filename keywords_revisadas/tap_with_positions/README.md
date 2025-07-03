# Tap With Positions — Native AppiumLibrary Keyword

The `Tap With Positions` keyword is the recommended native method for performing absolute screen touches, supporting multiple simultaneous touch points (multitouch) and configurable press duration.

---

## Purpose

To standardize, simplify, and strengthen coordinate-based tapping within the project by adopting a reliable, native approach instead of custom scripts.

---

## How It Works (overview)

This keyword accepts one or more coordinate pairs `[x, y]` and performs a tap action for a defined duration in milliseconds. It supports both simple and complex interactions, including multitouch gestures.

---

## Reason for Replacing the Custom `Perform Click A Point` Keyword

Although a custom `Perform Click A Point`keyword was previously developed for the project, it has been deprecated in favor of the native `Tap With Positions` keyword, which offers:

- Official support maintained by AppiumLibrary
- Multitouch with up to 5 fingers
- Better performance
- Reduced maintenance

📂 The original script (`perform_click_a_point_en.py`) has been retained for technical reference only.

---

## Arguments

| Argument   | Type  | Default | Description                                   |
|------------|-------|---------|-----------------------------------------------|
| `location` | list of [x, y] | –   | List of coordinate pairs for each touch point (up to 5)|
| `duration` | int            | 500 | Duration of the press in milliseconds                  |

---

## Usage Examples

### Single Tap in the Center of the Screen
```robot
Tap With Positions    200    [540, 960]
```

### Simultaneous Tap with Two Fingers
```robot
Tap With Positions    300    [200, 1000]    [600, 1000]
```

### Consecutive Taps at Different Points
```robot
Tap With Positions    100    [150, 1400]
Tap With Positions    100    [400, 1400]
Tap With Positions    100    [650, 1400]
```

---

## Test Structure

The test suite created to validate `Tap With Positions` includes:

- **Tapping specific areas (center, top-right corner)**
- **Error validation with invalid arguments**
- **Simultaneous multitouch execution**
- **Stress testing with 100 random interactions**

---

## Best Practices

- Prefer using variables ([`${x}`, `${y}`]) or lists ([`${x}`, `${y}`]) instead of hardcoded coordinates
- Always wait for the UI to respond after a tap:
  ```robot
  Wait Until Page Contains Element    xpath=//*    timeout=10s
  ```
- For long loops, monitor the app's state after every X iterations
- Use `Suite Setup` and `Suite Teardown` to maintain clean and reusable test suites

---

## Custom Keyword Reference

To review or test the previous implementation, see the legacy file:

```
/keywords_revisadas/perform_click_a_point_en.py
```