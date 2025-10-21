*** Settings ***

Library     AppiumLibrary
Library     ScrollToElement.py
Library     OperatingSystem
Library     DateTime

*** Variables ***
${START}    QAX
${DEVICE_NAME}    RX2N7004Y2T
*** Keywords ***

Start session Google Docs
    Open Application    http://localhost:4723
...    platformName=Android 
...    deviceName=${DEVICE_NAME}     #AndroidDevice
...    automationName=UiAutomator2
...    appPackage=com.google.android.apps.docs.editors.docs
...    appActivity=com.google.android.apps.docs.editors.kix.KixEditorActivity
...    noReset=true



Start session Tela Inicial
    Open Application    http://localhost:4723
...    platformName=Android 
...    deviceName=${DEVICE_NAME}     #AndroidDevice
...    automationName=UiAutomator2
...    appPackage=com.sec.android.app.launcher
...    appActivity=com.sec.android.app.launcher.activities.LauncherActivity
...    noReset=true

Start session Calendario
    Open Application    http://localhost:4723
...    platformName=Android 
...    deviceName=${DEVICE_NAME}     #AndroidDevice
...    automationName=UiAutomator2
...    appPackage=com.samsung.android.calendar
...    appActivity=com.samsung.android.app.calendar.activity.MainActivity
...    noReset=true

Start session Samsung Notes
    Open Application    http://localhost:4723
...    platformName=Android
...    deviceName=${DEVICE_NAME}     #AndroidDevice
...    automationName=UiAutomator2
...    appPackage=com.samsung.android.app.notes
...    appActivity=com.samsung.android.app.notes.memolist.MemoListActivity
...    noReset=true

Start session Calculadora
    Open Application
    ...    http://localhost:4723
    ...    platformName=Android
    ...    deviceName=AndroidDevice
    ...    automationName=UiAutomator2
    ...    app=${EXECDIR}/app/Calculator2.apk
    ...    noReset=true

Handle Backup if Prompt is Visible

    ${backup_prompt_visible}    Run Keyword And Return Status
    ...    Wait Until Page Contains Element    //*[contains(@text, "Get started")]    5s
    
    Run Keyword If    ${backup_prompt_visible}    Process Backup Prompt

Start session Youtube
        Open Application    http://localhost:4723
    ...    platformName=Android
    ...    appium:deviceName=AndroidDevice
    ...    appium:automationName=UIAutomator2
    ...    appium:appPackage=com.google.android.youtube
    ...    appium:appActivity=.HomeActivity
    ...    appium:autoGrantPermissions=true
    ...    appium:noReset=false
    ...    appium:ensureWebviewsHavePages=true
    ...    appium:nativeWebScreenshot=true
    
Start session Camera
    Open Application    http://localhost:4723
    ...    platformName=Android
    ...    deviceName=AndroidDevice
    ...    automationName=UIAutomator2
    ...    appPackage=com.android.camera2
    ...    appActivity=com.android.camera.CameraActivity
    ...    autoGrantPermissions=true
    ...    noReset=true

Start session 
    Open Application                 http://localhost:4723
    ...                              platformName=Android
    ...                              deviceName=Android Emulator
    ...                              automationName=UIAutomator2
    ...                              app=${EXECDIR}/app/yodapp-beta.apk
    ...                              autoGrantPermissions=true

    
Start session Google Maps

    Open Application    http://localhost:4723    
    ...    platformName=Android    
    ...    deviceName=AndroidDevice   
    ...    automationName=UIAutomator2
    ...    appPackage=com.google.android.apps.maps
    ...    appActivity=com.google.android.maps.MapsActivity
    ...    autoGrantPermissions=true

Start session Google Photos

    Open Application    http://localhost:4723    
    ...    platformName=Android    
    ...    deviceName=AndroidDevice    
    ...    automationName=UIAutomator2
    ...    appPackage=com.google.android.apps.photos
    ...    appActivity=.home.HomeActivity
    ...    autoGrantPermissions=true

Start session 99

    Open Application    http://localhost:4723
    ...    platformName=Android
    ...    deviceName=AndroidDevice
    ...    automationName=UIAutomator2
    ...    appPackage=com.taxis99
    ...    appActivity=com.didi.sdk.splash.SplashActivity
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