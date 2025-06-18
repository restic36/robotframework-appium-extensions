*** Settings ***

Library    AppiumZoomTreinamento.py
Library    AppiumPinchTreinamento.py
Library    AppiumLibrary

*** Keywords ***

Start session Google Maps

    Open Application    http://localhost:4723    
    ...    platformName=Android    
    ...    deviceName=Android Emulator    
    ...    automationName=UIAutomator2
    ...    appPackage=com.google.android.apps.maps
    ...    appActivity=com.google.android.maps.MapsActivity
    ...    udid=emulator-5554
    ...    autoGrantPermissions=true