# Perform Pinch Gesture — AppiumLibrary Extension

**Perform Pinch Gesture** is a custom keyword designed to simulate a realistic pinch-in gesture (zoom out) on Android devices during tests using **Appium** and **Robot Framework**.  
It supports both element-targeted pinching and full-screen gestures, with adjustable parameters for scale, duration, and movement direction.

---

## Purpose

- Perform realistic multi-touch pinch-in (zoom-out) gestures in automated mobile UI tests  
- Support both vertical and horizontal pinch directions  
- Allow pinching on specific elements or at screen center when no locator is provided  
- Ensure gesture coordinates stay within screen boundaries to prevent failures  
- Add small configurable pauses and interpolation steps to mimic human-like interaction  
- Provide clear logging for debugging and test reproducibility  

---

## How It Works

The keyword uses **W3C Touch Actions** through Selenium’s `ActionChains` API to simulate two fingers moving **towards** each other starting from positions apart from the center.

### Gesture Center:
- If **locator** is provided, the center is the middle of the target element.  
- If no **locator** is provided, the gesture starts at the screen center.  

### Finger Start Positions:
- Two touch points are placed apart based on `scale × movement` vertically or horizontally from the center.  

### Finger End Positions:
- Brought closer together (10px offset) towards the center.  
- Adjusted to remain inside screen bounds.  

### Interpolation Steps:
- The gesture moves in small increments, with optional pause before movement begins.  

### Execution:
- Both fingers touch down simultaneously, move towards each other over the given duration, and lift up.

---

## Parameters

| Argument  | Type       | Default     | Description |
|-----------|-----------|-------------|-------------|
| locator   | str \| None | None | Locator of the element to pinch on. If None, uses screen center. |
| scale     | float      | 0.5 | Pinch scale factor (0.1 ≤ scale < 1.0 required). |
| duration  | int        | 500 | Gesture duration in milliseconds. |
| direction | str        | "vertical" | Gesture direction: `"vertical"` or `"horizontal"`. |
| movement  | int/float  | 400 | Distance in pixels each finger starts from the center. |
| pause     | float      | 0.1 | Pause in seconds before movement starts. |
| steps     | int        | 50 | Number of interpolation steps for gesture realism. |

---

## Example

```robot
*** Settings ***
Library    GesturePinch.py

*** Test Cases ***
Pinch On Element
    Perform Pinch Gesture    locator=id=map_view    scale=0.6    duration=800    direction=vertical

Pinch On Screen Center
    Perform Pinch Gesture    scale=0.7    direction=horizontal    movement=300

```

# How to Execute

Run your Robot Framework test file:

```bash

robot PinchGesture.robot

```
Make sure:

- AppiumLibrary and GesturePinch are correctly imported.

- The emulator or physical device is connected and recognized by Appium.

- The app screen is in the correct state to receive a pinch gesture.

# Technical Details

- Built to work with AppiumLibrary and Robot Framework.

- Uses Selenium’s ActionChains with W3C Pointer Actions for multi-touch simulation.

- Supports both element-specific and screen-wide gestures.

- Automatically adjusts finger coordinates to avoid going outside the device’s visible bounds.

- Validates all input arguments for correctness before execution.