# Scroll Element Library

A custom library for **Robot Framework** and **Appium**, designed to execute *scroll/swipe* gestures **inside specific UI elements** of mobile applications.  
It provides **precise control over direction, distance, and speed**, ensuring reliable interactions even within internal areas of complex elements.

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
The `Scroll Inside` keyword is a *wrapper* for the **`mobile: swipeGesture`** Appium command, enabling:
- Element location via different strategies (`id`, `xpath`, `accessibility_id`, etc.).
- Direction control (`up`, `down`, `left`, `right`).
- Scroll percentage within the element.
- Gesture speed adjustment.

This approach prevents imprecise full-screen scrolls by interacting **only with the target element**.

---

## Prerequisites
- **Python** 3.7+
- **Appium Server** installed and running.
- **Robot Framework**:
  ```bash
  pip install robotframework
  ```
- **AppiumLibrary** for Robot Framework:
  ```bash
  pip install robotframework-appiumlibrary
  ```

---

## Installation
1. Add the `scroll.py` file to your test project directory.
2. Import the library into your `.robot` file:
   ```robot
   Library    scroll.py
   Library    AppiumLibrary
   ```

---

## Usage
### Syntax
```robot
Scroll Inside    <locator>    direction=<up|down|left|right>    percent=<0.01-1.0>    speed=<ms>
```

### Supported Locator Formats
- `id=com.example:id/my_element`
- `xpath=//android.widget.TextView[@text="Example"]`
- `accessibility_id=MyElement`
- `class_name=android.widget.Button`
- `android_uiautomator=new UiSelector().text("Example")`
- `ios_predicate=name == "Example"`
- `ios_class_chain=**/XCUIElementTypeButton[`name == "Example"`]`

You can also pass just `//my/xpath`, which will be automatically interpreted as `xpath=...`.

---

## Parameters
| Name         | Type  | Required | Default | Description |
|--------------|-------|----------|---------|-------------|
| `locator`    | str   | ✅       | —       | Locator of the target element |
| `direction`  | str   | ❌       | `down`  | Scroll direction (`up`, `down`, `left`, `right`) |
| `percent`    | float | ❌       | `0.75`  | Scroll distance percentage (0.01 to 1.0) |
| `speed`      | int   | ❌       | `800`   | Gesture speed in milliseconds |

---

## Usage Examples
```robot
*** Settings ***
Library    scroll.py
Library    AppiumLibrary

*** Test Cases ***
Scroll Down by XPath
    Scroll Inside    xpath=//android.widget.ScrollView    direction=down

Scroll Up by ID with Custom Speed
    Scroll Inside    id=com.example:id/list    direction=up    percent=0.5    speed=1000
```

---

## Notes
- `Scroll Inside` works **only within the located element**, not the entire screen.
- The `mobile: swipeGesture` command is compatible with Appium drivers that support **W3C Actions**.
- Very low `percent` values may result in imperceptible gestures.

---

## License
This project is free to use, modify, and distribute for personal or commercial purposes.
