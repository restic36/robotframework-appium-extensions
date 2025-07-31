*** Settings ***

Library     AppiumLibrary
Library     ./ClickElements.py

*** Keywords ***
Start session Calculator
    Open Application            http://localhost:4723
    ...                         automationName=UIAutomator2
    ...                         platformName=Android
    ...                         DeviceName=Emulator
    ...                         udid=emulator-5554
    ...                         autoGrantPermissions=true
    ...                         appPackage=com.google.android.calculator
    ...                         appActivity=com.android.calculator2.Calculator
    ...                         noReset=true


Close session
    Close Application