# ClickC — AppiumLibrary Extension

ClickC is a custom keyword that performs precise clicks on elements during tests with Appium and Robot Framework, using the W3C Actions API to control the exact touch position on the screen.
It offers flexibility in click positioning, allowing you to define absolute offsets (in pixels) or relative offsets (as a percentage of the element size).

## Purpose
- Perform pixel-perfect clicks on elements, controlling the exact point within the element area.
- Allow the use of relative offsets (% of element size) or absolute offsets (px).
- Ensure the click is executed within the screen boundaries.
- Increase compatibility and reliability of tests on real devices and emulators.
- Replace Appium's standard click methods with a more controlled approach via W3C Actions.

## How It Works
The keyword receives:

- `locator`: element identifier (any format supported by AppiumLibrary, such as id, xpath, accessibility id, etc.).
- `xoffset` (optional): horizontal click offset.
	- Value between 0 and 1 → interpreted as a percentage of the element's width.
	- Value greater than 1 → interpreted as pixels.
	- Default: 0.5 (center of the element).
- `yoffset` (optional): vertical click offset, with the same rule as xoffset.
	- Default: 0.5 (center of the element).

Execution flow:
1. Gets the current Appium driver instance.
2. Locates the element using AppiumLibrary.get_webelement(locator).
3. Gets the element's position and size (location, size).
4. Converts xoffset and yoffset to pixels, considering whether the value is percentage or absolute.
5. Calculates the final click coordinates (x, y).
6. Checks if the coordinates are within the screen boundaries.
7. Performs the click using W3C Actions (PointerInput and ActionBuilder).
8. Waits briefly (0.2s) between pointer_down and pointer_up.
9. Logs detailed information about each step for debugging.

## How To Execute
To run all tests:
```shell
robot ClickC.robot
```

Prerequisites:
- AppiumLibrary imported and configured.
- Device/emulator connected to the Appium server.
- ClickC keyword imported.

Example usage in a `.robot` file:
```robotframework
*** Settings ***
Library    AppiumLibrary
Library    Appiumclick.py

*** Test Cases ***
Click In The Center Of The Button
		Open Application    http://localhost:4723/wd/hub    platformName=Android    deviceName=emulator-5554    appPackage=com.example    appActivity=.MainActivity
		ClickC    id=com.app.example:id/botao_confirmar

Click At Specific Point
		ClickC    xpath=//android.widget.TextView[@text="OK"]    10    25
```

## Technical Details
- Based on the W3C Actions API from Selenium WebDriver (ActionBuilder and PointerInput).
- Accepts relative and absolute offsets for clicking.
- Checks if the driver is active before execution.
- Confirms that the calculated point is within the screen before clicking.
- Works on Android and iOS (as long as Appium supports W3C Actions for the driver used).

## Code Structure
Class: `Appiumclick`
- Methods:
	- `_driver`: returns the current driver instance.
	- `clickC(locator, xoffset, yoffset)`: performs the precise click.
- Scope: Global (loaded as a Robot Framework library).
- Detailed logging of each process step for easier debugging.

## Test Structure
The keyword was validated in:
- **Mocked Tests**
	- Click in the center of the element — default offsets (0.5, 0.5).
	- Click with pixel offsets — xoffset=30, yoffset=50.
	- Click with percentage offsets — xoffset=0.25, yoffset=0.75.
	- Non-existent element — raises exception with detailed message.
	- Out-of-bounds coordinates — fails with ValueError.
- **Emulator Tests**
	- Click on central and side buttons.
	- Click on small elements with specific offsets.
	- Click on scroll areas to trigger gestures.
- **Physical Device Tests (Pending)**
	- Not yet tested on real devices, but compatible with any device supported by Appium.
