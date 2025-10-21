*** Settings ***

Library     AppiumLibrary
Library     ScrollToElement.py
Library     OperatingSystem
Library     DateTime

*** Keywords ***

Open Home Screen
    Open Application    http://localhost:4723
...    platformName=Android 
...    deviceName=AndroidDevice
...    automationName=UiAutomator2
...    appPackage=com.google.android.apps.nexuslauncher
...    appActivity=com.google.android.apps.nexuslauncher.NexusLauncherActivity
...    noReset=true