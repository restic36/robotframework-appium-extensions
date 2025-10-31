# Robot Framework - Appium Extensions (Android)

Custom keywords extending [Robot Framework’s AppiumLibrary](https://github.com/serhatbolsu/robotframework-appiumlibrary), optimized for **mobile automation on Android**.

This library enhances the native AppiumLibrary with new gestures, UI utilities, and validation features designed for **QA teams automating Android applications**.  
It aims to serve as an open-source reference for improving test reliability, coverage, and maintainability in mobile test automation.

[![PyPI version](https://img.shields.io/pypi/v/robotframework-appium-extensions.svg)](https://pypi.org/project/robotframework-appium-extensions/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/downloads/)

---

## Available Keywords

- Gestures:
    - Scroll Inside
    - Scroll To Element
    - Swipe Element
    - Perform Long Press
    - Perform Pinch
    - Perform Zoom

- Touch utilities:
    - Click Elements
    - Tap At Percentage
    - Tap Element At Coordinates

- Visibility & Lookup:
    - Compare Screenshots
    - Get Visible Elements On Screen
    - Wait Multiple Elements

- System/App:
    - Change Theme
    - Get Readable Network Status
    - Terminate Application Extension

Individual documentation are in keyword docstrings.

---

## Technology Stack

- **Python 3.9+**
- **Robot Framework 4.0+**
- **Appium Server 2.0**
- **UiAutomator2 driver (Android) 4.x**
- **Appium-Python-Client >=3.1.0,<5.0.0**
- **Selenium W3C Actions**
- **OpenCV + scikit-image + NumPy** (for visual comparison)
- **ADB + Android SDK tools**

---

## Prerequisites and Requirements

- Android device or emulator connected with ADB
- Dependencies listed in `requirements.txt`
- Appium Server running (`appium` or `appium --allow-cors`)
    ```bash
  npm install -g appium
    ```
- UiAutomator2 driver installed (`appium driver install uiautomator2`)
    ```bash
  appium driver install uiautomator2
    ```

---

## Installation

You can install the package directly from **PyPI** (recommended):
```bash
pip install robotframework-appium-extensions
```

Or, if you prefer to work with the latest development version:
```bash
git clone https://github.com/restic36/robotframework-appium-extensions.git
cd robotframework-appium-extensions
pip install .
```

---

## How To Run Tests

Run any .robot test suite using Robot Framework’s CLI:
```bash
robot -d results tests/robot/perform_zoom.robot
```
- `-d results` saves logs, reports, and screenshots in a dedicated folder.
- You can adapt paths for your test files or custom resources.

---

## Emulator / Device Setup

To successfully run the automated tests included in this repository, ensure that the test environment (emulator or physical device) meets the following conditions:
- Use an **Android device or emulator** running **Android 11 or higher**.  
- Before executing the test suites, **verify which applications are required** by the selected tests and ensure they are **properly installed** on the device.  
  > For example: some suites may require system apps such as Calculator, Google Maps, or Play Store.
- Using a **Google APIs emulator image** is recommended, as minimal system images may lack these default apps.

---

## Usage Example

```robot
*** Settings ***
Library    AppiumLibrary
Library    robotframework_appium_extensions.keywords.PerformPinch

*** Test Cases ***
Pinch Example
    Open Application    http://localhost:4723    platformName=Android    automationName=UiAutomator2
    Perform Pinch    locator=id=map_view    scale=0.6
```

---

## Known Limitations

- Platform: tested on Android 7.0+; iOS not supported.
- Multi-touch gestures: Android 9+ recommended for reliable Pinch/Zoom (W3C Actions).
- Device fragmentation: differences between manufacturers (Samsung/Xiaomi, etc.) may affect gesture behavior.
- Dynamic elements: fast-moving/animated elements may require explicit waits.
- Power saving mode: can cause inconsistencies; disable during tests.
- Performance: image comparison may be slow on high-resolution screens.

---

## Troubleshooting

- Device not detected: run adb devices → enable USB Debugging; restart ADB (`adb kill-server && adb start-server`).
- Appium session not starting: ensure Appium 2.x is running and uiautomator2 driver installed (`appium driver install uiautomator2`).
- Element not found: validate selectors in Appium Inspector; prefer `id/accessibility_id`; use explicit waits.
- Inconsistent gestures: increase `duration/steps`; add pauses (`pause_before/pause_after`); prefer Android 9+.
- Slow/timeouts: use a good-quality USB cable; disable Android animations; increase timeouts; close background apps.
- ADB errors: ensure `adb` is in your PATH; restart ADB; reconnect the device; check permissions.

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Code style
- Commit messages
- Tests and documentation
- PR process

---

## License

Licensed under Apache 2.0 [LICENSE](LICENSE)

---

### Acknowledgments

This open-source repository was developed within the scope of the **Technology Residency Program**,  
executed by **CEPEDI**, coordinated by **SOFTEX**, and supported by the **Ministry of Science, Technology and Innovation (MCTI)**.

The development challenge addressed in this repository was proposed by **Positivo Tecnologia**,  
a partner company of the program, as part of its collaboration with the Technology Residency initiative.

We acknowledge and thank all the institutions involved for their support in the execution and dissemination of this open-source project.
