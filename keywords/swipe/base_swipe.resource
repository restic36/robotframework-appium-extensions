*** Settings ***
Library    AppiumLibrary
Library    swipe.py

*** Keywords ***
Start session Rgb
    Open Application    http://localhost:4723
    ...    platformName=Android
    ...    deviceName=Android Emulator
    ...    automationName=UIAutomator2
    ...    appPackage=henry.rgb.color.picker
    ...    appActivity=.MainActivity
    ...    udid=emulator-5554
    ...    autoGrantPermissions=true