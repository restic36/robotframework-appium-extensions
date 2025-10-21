# Perform Zoom Gesture — AppiumLibrary Extension

**Perform Zoom Gesture** is a custom keyword designed to simulate a realistic pinch-out (zoom in) gesture on Android devices during tests using Appium and Robot Framework. It supports both element-targeted zooming and full-screen gestures, with adjustable parameters for scale, duration, and movement direction.

---

## Purpose

- Perform realistic multi-touch zoom-in gestures in automated mobile UI tests  
- Support both vertical and horizontal zoom directions  
- Allow zooming on specific elements or at screen center when no locator is provided  
- Ensure gesture coordinates stay within screen boundaries to prevent failures  
- Add small configurable pauses and interpolation steps to mimic human-like interaction  
- Provide clear logging for debugging and test reproducibility  

---

## How It Works

The keyword uses **W3C Touch Actions** through Selenium’s **ActionChains API** to simulate two fingers moving away from each other starting from a common center point.

### Gesture Center
- If **locator** is provided, the center is the middle of the target element.  
- If no locator is provided, the gesture starts at the screen center.  

### Finger Start Positions
- Two touch points are placed slightly apart (**offset = 10px**) vertically or horizontally from the center.  

### Finger End Positions
- Calculated based on `scale × movement`, then adjusted to remain inside screen bounds.  

### Interpolation Steps
- The gesture moves in small increments, with optional pause before movement begins.  

### Execution
- Both fingers touch down simultaneously, move away over `duration` milliseconds, and lift up.  

---

## Parameters

| Argument   | Type        | Default  | Description |
|------------|------------|----------|-------------|
| locator    | str \| None | None     | Locator of the element to zoom in on. If None, uses screen center. |
| scale      | float       | 1.5      | Zoom scale factor (> 1.0 required). |
| duration   | int         | 500      | Gesture duration in milliseconds. |
| direction  | str         | "vertical" | Gesture direction: `"vertical"` or `"horizontal"`. |
| movement   | int/float   | 300      | Distance in pixels each finger moves from the center. |
| pause      | float       | 0.1      | Pause in seconds before movement starts. |
| steps      | int         | 50       | Number of interpolation steps for gesture realism. |

---

## Example

```robotframework
*** Settings ***
Library    GestureZoom.py

*** Test Cases ***
Zoom On Element
    Perform Zoom Gesture    locator=id=map_view    scale=2.0    duration=800    direction=vertical

Zoom On Screen Center
    Perform Zoom Gesture    scale=1.8    direction=horizontal    movement=250
