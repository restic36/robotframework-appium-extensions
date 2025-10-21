*** Settings ***

Library     AppiumLibrary
Library     GesturePinch.py
Library     OperatingSystem
Library     DateTime

*** Variables ***

*** Keywords ***

Start session Google Maps

    Open Application    http://localhost:4723    
    ...    platformName=Android    
    ...    deviceName=AndroidDevice   
    ...    automationName=UIAutomator2
    ...    appPackage=com.google.android.apps.maps
    ...    appActivity=com.google.android.maps.MapsActivity
    ...    autoGrantPermissions=true