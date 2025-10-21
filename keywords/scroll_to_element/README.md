# ScrollToElement Keyword

## Overview
The `ScrollToElement` keyword provides a robust and configurable way to scroll vertically or horizontally until a specific element becomes visible on the screen.  
It is designed to work with **AppiumLibrary** in **Robot Framework**, supporting both full-screen and container-based scroll gestures.  
The implementation ensures smooth, realistic scrolling while respecting screen bounds and limiting the number of swipe attempts.

---

## Features
- Scroll **vertically** or **horizontally** (`up`, `down`, `left`, `right`)
- Optionally scroll **within a specific container element**
- **Visibility detection** to stop scrolling once the element appears
- Configurable:
  - Maximum number of swipes
  - Swipe distance ratio
  - Swipe duration
- Adjusts coordinates to **stay within screen bounds**
- Uses **W3C Touch Actions** for precise gesture simulation

---

## Keyword Signature
```robotframework

Scroll To Element

```
# Arguments

| Argument               | Type    | Required | Default  | Description                                                                        |
| ---------------------- | ------- | -------- | -------- | ---------------------------------------------------------------------------------- |
| `locator`              | `str`   | Yes      | -        | Locator of the target element. Format: `strategy=value` (e.g., `id=login-button`). |
| `max_swipes`           | `int`   | No       | `5`      | Maximum number of swipe attempts before failing.                                   |
| `direction`            | `str`   | No       | `"down"` | Direction of scrolling: `"down"`, `"up"`, `"left"`, `"right"`.                     |
| `swipe_distance_ratio` | `float` | No       | `0.4`    | Fraction of screen or container size to swipe (0.1 to 0.99).                       |
| `duration`             | `int`   | No       | `500`    | Duration of each swipe in milliseconds.                                            |
| `container_locator`    | `str`   | No       | `None`   | Locator of a container element to restrict scrolling within.                       |

# Example Usage

## Scroll full screen until element is visible

```robot
*** Settings ***
Library    AppiumLibrary
Library    ScrollToElement.py

*** Test Cases ***
Scroll To Login Button
    Scroll To Element    id=login-button
```

## Scroll within a container element

```robot
*** Settings ***
Library    AppiumLibrary
Library    ScrollToElement.py

*** Test Cases ***
Scroll To Login Button
    Scroll To Element    id=login-button
```

# How It Works

## Determine Scroll Area

- If container_locator is provided, scrolling is limited to that element’s bounds.

- Otherwise, scrolling uses the entire screen.

## Calculate Swipe Coordinates

- Based on direction and swipe_distance_ratio.

- Ensures coordinates remain within screen boundaries.

## Perform Scroll Gesture

- Simulates a realistic finger swipe using W3C Touch Actions.

- Interpolates multiple steps for smoothness.

## Visibility Check

- After each swipe, checks if the target element is now visible.

- Stops immediately if found; otherwise, continues until max_swipes is reached.