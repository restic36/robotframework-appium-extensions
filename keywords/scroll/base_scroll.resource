*** Settings ***
Library    AppiumLibrary
Library    scroll.py

*** Keywords ***
Start session Play Store
    Open Application    http://localhost:4723
    ...    platformName=Android
    ...    deviceName=Android Emulator
    ...    automationName=UIAutomator2
    ...    appPackage=com.android.vending
    ...    appActivity=com.android.vending.AssetBrowserActivity
    ...    udid=emulator-5554
    ...    autoGrantPermissions=true

Start session Timer
    Open Application    http://localhost:4723
    ...    platformName=Android
    ...    deviceName=Android Emulator
    ...    automationName=UIAutomator2
    ...    appPackage=com.digitalchemy.timerplus
    ...    appActivity=com.digitalchemy.timerplus.ui.main.MainActivity
    ...    udid=emulator-5554
    ...    autoGrantPermissions=true
