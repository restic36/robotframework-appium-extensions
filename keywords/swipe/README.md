# Swipe Element Library

A custom library for **Robot Framework** and **Appium**, designed to perform swipe (drag gesture) actions on elements within the UI of mobile applications.  
Developed to provide greater control over gesture direction, distance, and speed, avoiding inaccurate interactions near element edges.

---

## Table of Contents
1. [Overview](#overview)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Parameters](#parameters)  
6. [Usage Examples](#usage-examples)  
7. [Notes](#notes)  
8. [License](#license)

---

## Overview
The `Swipe Element` keyword is a wrapper for the **`mobile: dragGesture`** Appium command, allowing:
- Locating elements via different strategies (`id`, `xpath`, `accessibility_id`, etc.)
- Defining the direction (`up`, `down`, `left`, `right`)
- Controlling the displacement percentage (including values greater than 100%)
- Adjusting gesture speed
- Setting an initial margin to avoid touches on element edges

---

## Prerequisites
- **Python** 3.7+
- **Appium Server** installed and running
- **Robot Framework** installed:
  ```bash
  pip install robotframework
  ```
- **AppiumLibrary** for Robot Framework:
  ```bash
  pip install robotframework-appiumlibrary
  ```

---

## Installation
1. Add the `swipe.py` file to your test project directory.
2. Import the library into your `.robot` file:
   ```robot
   Library    swipe.py
   Library    AppiumLibrary
   ```

---

## Usage
### Syntax
```robot
Swipe Element    <locator>    direction=<up|down|left|right>    percent=<0.01-2.0>    speed=<ms>
```

### Supported Locator Formats
- `id=com.example:id/my_element`
- `xpath=//android.widget.TextView[@text="Example"]`
- `accessibility_id=MyElement`
- `class_name=android.widget.Button`
- `android_uiautomator=new UiSelector().text("Example")`
- `ios_predicate=name == "Example"`
- `ios_class_chain=**/XCUIElementTypeButton[`name == "Example"`]`

---

## Parameters
| Name         | Type  | Required | Default | Description |
|--------------|-------|----------|---------|-------------|
| `locator`    | str   | ✅       | —       | Locator of the target element |
| `direction`  | str   | ❌       | `right` | Swipe direction (`up`, `down`, `left`, `right`) |
| `percent`    | float | ❌       | `0.5`   | Displacement percentage (0.01 to 2.0) |
| `speed`      | int   | ❌       | `800`   | Gesture speed in milliseconds |

---

## Usage Examples
```robot
*** Settings ***
Library    swipe.py
Library    AppiumLibrary

*** Test Cases ***
Swipe Right
    Swipe Element    xpath=//android.widget.TextView[@text="Example"]    direction=right    percent=0.8    speed=500

Swipe Down Using ID
    Swipe Element    id=com.example:id/list    direction=down    percent=1.5    speed=800
```

---

## Notes
- The `percent` parameter can exceed `1.0` to allow the swipe to go beyond the element’s size.
- A fixed **5%** starting margin is applied to prevent gestures from starting at the edges.
- The `mobile: dragGesture` command requires the Appium driver to use **W3C Actions**.

---

## License
This project is free to use, modify, and distribute for personal or commercial purposes.
