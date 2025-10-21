# Terminate Application — AppiumLibrary Extension

`TerminateApplicationExtension` is a custom keyword library built to extend AppiumLibrary with functionality for terminating Android applications during automated testing using Robot Framework. It provides utilities to close apps and adictionaly retrieve the current app package ID in active Appium sessions.

---

## 🎯 Purpose

- Programmatically terminate an Android application during test execution
- Retrieve the current app identifier (`appPackage`) without hardcoding it

---

## ⚙️ How It Works

This extension leverages Appium's native `driver.terminate_app(app_id)` method to close the specified application.  
The `Get Current App Id` keyword reads the `appPackage` from the current session's capabilities, allowing tests to be dynamic and environment-independent.

---

## 📦 How To Execute

To run the tests:

```bash
robot TerminateApplicationTest.robot
```

Make sure that:
- The Appium server is running (`http://localhost:4723/wd/hub`)
- An Android emulator or real device is connected
- Your test environment and `desiredCapabilities` are correctly configured

---

## 🧠 Technical Details

- Built using Robot Framework and AppiumLibrary
- Implemented as a Python class with `ROBOT_LIBRARY_SCOPE = GLOBAL`
- `terminate_application` takes an app ID (e.g., `com.example.myapp`) and closes it
- `get_current_app_id` accesses the current session and retrieves the running app's package name

---

## 📁 Code Structure

### Python Library
- **`TerminateApplicationExtension.py`**
  - `terminate_application(app_id)` — terminates the given app via Appium
  - `get_current_app_id()` — retrieves the `appPackage` from current session

### Robot Framework Files
- **`TerminateApplicationTest.robot`**
  - Test suite using the custom keywords
- **`base.resource`**
  - Shared resource file with reusable keyword logic

---

## ✅ Test Scenarios

### Simulated
- Opened YouTube and performed multiple vertical swipes to simulate prolonged usage
- Opened TikTok and executed continuous vertical scrolls to replicate heavy user interaction
- After repeated swipes, invoked Terminate Application to test app closure under load

---

## 📚 Requirements

- [AppiumLibrary](https://robotframework.org/AppiumLibrary/)
- [Appium Server](https://appium.io/)
- Python 3.7+
- Android Emulator or Real Device
