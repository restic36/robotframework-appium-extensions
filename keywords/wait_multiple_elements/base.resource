*** Settings ***

Library     AppiumLibrary
Library     ./WaitMultipleElements.py

*** Keywords ***
Start Session Store
    Open Application    http://localhost:4723
    ...                 automationName=UIAutomator2
    ...                 platformName=Android
    ...                 deviceName=Emulator
    ...                 udid=emulator-5554
    ...                 autoGrantPermissions=true
    ...                 appPackage=com.android.vending
    ...                 appActivity=com.android.vending.AssetBrowserActivity

Close session
    Close Application