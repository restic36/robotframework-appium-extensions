# Long Press Extension for Appium

Implementation of a Robot Framework keyword to perform a long press action on a web/app element using Selenium ActionChains

# Installation 

1-Place the AppiumLongPressExtensions class file (e.g., AppiumLongPressExtensions.py) in a Python package accessible by your Robot project.

2-Ensure Robot Framework and AppiumLibrary are installed

# Keyword: LongP

Performs a long press on the element found by locator, holding for the specified duration.

# Parameters

locator – locator of the target element in the format 'strategy=value' (required)

duration – duration of the long press in milliseconds (optional, default: 1000ms)

# Notes:

* Locator must be in the format 'strategy=value' (e.g., 'id=myButton', 'xpath=//button[@text="OK"]').

* Duration is specified in milliseconds and converted to seconds for ActionChains.

* Uses Selenium's ActionChains with click_and_hold() and release() methods.

* Requires AppiumLibrary instance available in Robot context.

* Raises descriptive exceptions if driver is absent, element not found, or locator format is invalid.