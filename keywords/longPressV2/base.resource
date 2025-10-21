*** Settings ***

Library     AppiumLibrary
Library     ./AppiumLongPressExtensions.py
Library     ./AppiumZoomExtensions.py
Library     OperatingSystem
Library     DateTime


*** Variables ***

${start}    QAX

*** Keywords ***
Start session
    Open Application                 http://localhost:4723
    ...                              platformName=Android
    ...                              deviceName=Android Emulator
    ...                              automationName=UIAutomator2
    ...                              appium:noReset=true       

Start session 1
      Open Application            http://localhost:4723
    ...                         automationName=UIAutomator2
    ...                         platformName=Android
    ...                         DeviceName=Emulator
    ...                         udid=emulator-5554
    ...                         autoGrantPermissions=true
    ...                         app=${EXECDIR}/app/Calculator2.apk  

Start session 2
        Open Application            http://localhost:4723
    ...                         automationName=UIAutomator2
    ...                         platformName=Android
    ...                         DeviceName=Emulator
    ...                         udid=emulator-5554
    ...                         autoGrantPermissions=true
    ...                         app=${EXECDIR}/app/yodapp-beta.apk
 
    


Get started
    Wait Until Page Contains         ${start}                              7
    Click Text                       ${start}

Navigate to
    [Arguments]                      ${item_text}
    ${hamburger}                     Set Variable                          xpath=//android.widget.ImageButton[@content-desc="Open navigation drawer"]

    Wait Until Element Is Visible    ${hamburger}                          5
    Click Element                    ${hamburger}

    ${menu_item}                     Set Variable                          xpath=//*[@resource-id="com.qaxperience.yodapp:id/navView"]//*[@text="${item_text}"]

    Wait Until Element Is Visible    ${menu_item}                          5
    Click Element                    ${menu_item}

Go to item
    [Arguments]                      ${item}                               ${checkpoint}
    Wait Until Page Contains         ${item}                               5
    Click Text                       ${item}
    Wait Until Page Contains         ${checkpoint}


Close session
    Close Application

Start session Google Maps

    Open Application    http://localhost:4723    
    ...    platformName=Android    
    ...    deviceName=Android Emulator    
    ...    automationName=UIAutomator2
    ...    appPackage=com.google.android.apps.maps
    ...    appActivity=com.google.android.maps.MapsActivity
    ...    udid=emulator-5554
    ...    autoGrantPermissions=true

Start session Google Photos

    Open Application    http://localhost:4723    
    ...    platformName=Android    
    ...    deviceName=Android Emulator    
    ...    automationName=UIAutomator2
    ...    appPackage=com.google.android.apps.photos
    ...    appActivity=.home.HomeActivity
    ...    udid=emulator-5554
    ...    autoGrantPermissions=true


