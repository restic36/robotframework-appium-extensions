*** Settings ***

Resource     ../resources/base.resource

*** Variables ***
${DURATION}      500

*** Keywords ***
Handle Backup Prompt If Visible
    Sleep    5
    ${backup_prompt_visible}    Run Keyword And Return Status
    ...    Wait Until Page Contains Element    //*[contains(@text, "Get started")]    5s
    Run Keyword If    ${backup_prompt_visible}    Process Backup Prompt

Process Backup Prompt
    Click Element    //android.widget.Switch[@resource-id="com.google.android.apps.photos:id/onboarding_toggle"]
    Wait Until Page Contains Element    //*[contains(@text, "Continue without backup")]    5s
    Click Element    //*[contains(@text, "Continue without backup")]
    Sleep    2s

*** Test Cases ***

Deve realizar um zoom no Google Maps
    [Tags]    maps
    Start session Google Maps
    Sleep    15
    Capture Page Screenshot    before_zoom.png
    Sleep    5

    ##### Tentativas e variações de comandos de zoom (comentadas) #####
    # Universal Zoom On Area with Bounds      id=com.google.android.apps.maps:id/mainmap_container               # Zoom In
    # Perform Pinch Gesture          # Zoom Out
    # ----- Funcionando -----
    # Zoom On Element by Coordinates   locator=com.google.android.apps.maps:id/mainmap_container    # scale=2.0    # duration_ms=100    pause_s=0.5    
    # Universal Zoom On Area_2    id=com.google.android.apps.maps:id/mainmap_container    scale=2.0    duration_ms=100
    # Universal Zoom On Area with Bounds      bounds=[166,733][456,499]
    # Universal Zoom On Area with Bounds      bounds=[166,733][622,1232]
    # Universal Zoom On Area    id=com.google.android.apps.maps:id/mainmap_container    scale=2.0    duration_ms=100
    # Force Zoom On Element    id=com.google.android.apps.maps:id/mainmap_container    scale=2.0    duration_ms=100    pause_s=0.5
    # Sleep    5
    # ---------------------
    
    Capture Page Screenshot
    Sleep    5
    Perform Pinch Gesture     id=com.google.android.apps.maps:id/mainmap_container
    Sleep    5
    Capture Page Screenshot

    # Zoom Java    id=com.google.android.apps.maps:id/mainmap_container

    Sleep    15
    Capture Page Screenshot    after_zoom.png
    Close session

Deve realizar um zoom em uma foto no Google Fotos
    [Tags]    zoom
    Start session Google Photos
    Handle Backup Prompt If Visible

    Wait Until Page Contains Element    //*[contains(@text, "Get 75% off your first 2 months")]
    Click Element    //android.widget.RadioButton[@resource-id="com.google.android.apps.photos:id/no_subscription_radio_button"]

    Wait Until Page Contains Element    //*[contains(@text, "Continue without subscription")]
    Click Element    //*[contains(@text, "Continue without subscription")]

    Wait Until Page Contains Element    //*[contains(@text, "Collections")]
    Click Element    //*[contains(@text, "Collections")]

    Wait Until Page Contains Element    //android.widget.TextView[@text="Screenshots"]
    Click Element    //android.widget.TextView[@text="Screenshots"]

    Wait Until Page Contains Element    //android.widget.ImageView[@content-desc="Photo taken on Mar 31, 2025 2:10 AM"]
    Click Element    //android.widget.ImageView[@content-desc="Photo taken on Mar 31, 2025 2:10 AM"]

    Wait Until Page Contains Element    //android.widget.ImageView[@content-desc="Edit"]
    Sleep    5
    Capture Page Screenshot

    Sleep    5
    Sleep    5
    Capture Page Screenshot
    Close session

Deve realizar um zoom no aplicativo da Camera
    [Tags]    camera
    Start session Camera
    Wait Until Page Contains Element    //android.widget.ImageView[@content-desc="Options"]
    Sleep    5
    Capture Page Screenshot

    Sleep    5
    Capture Page Screenshot
    Close session

Deve realizar um zoom no Youtube
    [Tags]    youtube
    Start session Youtube
    Wait Until Page Contains Element    //android.widget.Button[@content-desc="Library"]
    Click Element    //android.widget.Button[@content-desc="Library"]
    Sleep    60

Click Element At Specific Coordinates
    [tags]   android
    Start session Camera
    
    Wait Until Element Is Visible    xpath=//android.widget.ImageView[@content-desc="Shutter"]    5s

    ClickC     xpath=//android.widget.FrameLayout[@resource-id="com.android.camera2:id/mode_options_overlay"]     40    100
    Close session

Teste de clique longo
    [Tags]                      long

    Start session 
    Get started
    Navigate to                 Clique em Botões
    Go to item                  Clique longo                               Botão clique longo

    Clique longo                     id=com.qaxperience.yodapp:id/long_click    

    Wait Until Page Contains    Isso é um clique longo
    Capture Page Screenshot

    Close session


Deve poder fazer a conta 9+5 na calculadora com point_click
    [Tags]    addition
    Open Application    http://localhost:4723
    ...                 automationName=uiautomator2
    ...                 platformName=Android
    ...                 deviceName=Emulator
    ...                 udid=emulator-5554
    ...                 autoGrantPermissions=true
    ...                 appPackage=com.google.android.calculator
    ...                 appActivity=com.android.calculator2.Calculator
    ...                 noReset=true

    Point Click    ${670}    ${1350}    100
    Point Click    ${920}    ${1800}    100
    Point Click    ${420}    ${1500}    100
 
    Sleep    2
    
    Close Application


Deve realizar um Zoom e Pinch no Google Maps alternando orientação da direção
    [Tags]    pinchzoommaps
    Start session Google Maps
    Sleep    10

    #Wait Until Element Is Visible    //android.widget.Button[@content-desc="Entrar no modo de bússola"]
    #Click Element    //android.widget.Button[@content-desc="Entrar no modo de bússola"]
    Sleep    2

    Perform Pinch  id=com.google.android.apps.maps:id/mainmap_container    scale=0.7    duration=${DURATION}    steps=20    direction=horizontal
    Sleep    5 
    Perform Zoom  id=com.google.android.apps.maps:id/mainmap_container    scale=1.5    duration=${DURATION}    steps=50    direction=horizontal
    Sleep    5
    Perform Pinch  id=com.google.android.apps.maps:id/mainmap_container    scale=0.3    duration=${DURATION}    steps=20   direction=vertical
    Sleep    5     
    Perform Zoom   id=com.google.android.apps.maps:id/mainmap_container    scale=1.9    duration=${DURATION}    steps=50    direction=vertical
    Sleep    5
    Perform Zoom   id=com.google.android.apps.maps:id/mainmap_container    scale=1.6    duration=${DURATION}    steps=50    direction=horizontal
    Sleep    5

Deve realizar vários Pinch no Google Maps na direção vertical
    [Tags]    pinchmaps
    Start session Google Maps
    Sleep    10

    #Wait Until Element Is Visible    //android.widget.Button[@content-desc="Entrar no modo de bússola"]
    #Click Element    //android.widget.Button[@content-desc="Entrar no modo de bússola"]
    Sleep    2

    Perform Pinch Gesture  id=com.google.android.apps.maps:id/mainmap_container    scale=0.7    duration=${DURATION}    steps=20    direction=horizontal
    Sleep    5
    Perform Pinch Gesture  id=com.google.android.apps.maps:id/mainmap_container    scale=0.9    duration=${DURATION}    steps=20    direction=horizontal
    Sleep    5
    Perform Pinch Gesture  id=com.google.android.apps.maps:id/mainmap_container    scale=0.4    duration=${DURATION}    steps=20    direction=horizontal
    Sleep    5
    Perform Pinch Gesture  id=com.google.android.apps.maps:id/mainmap_container    scale=0.3    duration=${DURATION}    steps=20    direction=horizontal
    Sleep    5
    Perform Pinch Gesture  id=com.google.android.apps.maps:id/mainmap_container    scale=0.5    duration=${DURATION}    steps=20    direction=horizontal
    