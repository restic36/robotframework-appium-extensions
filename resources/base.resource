*** Settings ***

Library     click_point.py
Library     AppiumLibrary
Library     AppiumZoomExtensions.py
Library     AppiumLongPressExtensions.py
Library     AppiumZoomExtensions2.py
Library     AppiumZoomExtensions2_1.py
Library     AppiumZoomExtensions2_2.py
Library     AppiumZoomExtensions2_3.py
Library     AppiumZoomExtensions3.py
Library     AppiumZoomExtensions4.py
Library     AppiumZoomExtensions5.py
Library     AppiumPinchExtensions.py
Library     AppiumZoomExtensions2_4.py
Library     AppiumZoomExtensions6.py
Library     AppiumZoomExtensions6_1.py
Library     AppiumZoomExtensions6_2.py
Library     AppiumZoomExtensions_FINAL.py
Library     AppiumPinchExtensions_FINAL.py
Library     AppiumZoomExtensions7.py
Library     Appiumclick.py
Library     OperatingSystem
Library     DateTime

*** Variables ***
${START}    QAX

*** Keywords ***
Handle Backup if Prompt is Visible

    ${backup_prompt_visible}    Run Keyword And Return Status
    ...    Wait Until Page Contains Element    //*[contains(@text, "Get started")]    5s
    
    Run Keyword If    ${backup_prompt_visible}    Process Backup Prompt

Start session Youtube
        Open Application    http://localhost:4723
    ...    platformName=Android
    ...    appium:deviceName=Android Emulator
    ...    appium:automationName=UIAutomator2
    ...    appium:appPackage=com.google.android.youtube
    ...    appium:appActivity=.HomeActivity
    ...    appium:udid=emulator-5554
    ...    appium:autoGrantPermissions=true
    ...    appium:noReset=false
    ...    appium:ensureWebviewsHavePages=true
    ...    appium:nativeWebScreenshot=true
    
Start session Camera
    Open Application    http://localhost:4723
    ...    platformName=Android
    ...    deviceName=Android Emulator
    ...    automationName=UIAutomator2
    ...    appPackage=com.android.camera2
    ...    appActivity=com.android.camera.CameraActivity  # Activity principal encontrada
    ...    udid=emulator-5554
    ...    autoGrantPermissions=true
    ...    noReset=true
    
Start session 
    Open Application                 http://localhost:4723
    ...                              platformName=Android
    ...                              deviceName=Android Emulator
    ...                              automationName=UIAutomator2
    ...                              app=${EXECDIR}/app/yodapp-beta.apk
    ...                              uid=emulator-5554
    ...                              autoGrantPermissions=true

    
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

Get Started
    Wait Until Page Contains    ${START}
    Click Text                  ${START}
    
Navigate to 
    [Arguments]    ${item_text}
    ${hamburguer}    Set Variable    xpath=//android.widget.ImageButton[@content-desc="Open navigation drawer"]

    Wait Until Element Is Visible     ${hamburguer}
    Click Element                     ${hamburguer}
    
    ${menu_item}    Set Variable    xpath=//*[@resource-id="com.qaxperience.yodapp:id/navView"]//*[@text="${item_text}"]

    Wait Until Element Is Visible    ${menu_item}
    Click Element                    ${menu_item}

Go to item 
    [Arguments]    ${item}    ${checkpoint}
    Wait Until Page Contains    ${item}
    Click Text                  ${item}
    Wait Until Page Contains    ${checkpoint}
    
Test body
    Click Text                  CLIQUE SIMPLES
    Wait Until Page Contains    Isso é um clique simples

Close session
    Sleep     5
    Close Application 
    
Process Backup Prompt

    Click Element    //android.widget.Switch[@resource-id="com.google.android.apps.photos:id/onboarding_toggle"]
    Wait Until Page Contains Element    //*[contains(@text, "Continue without backup")]    5s
    Click Element    //*[contains(@text, "Continue without backup")]
    Sleep    2s    