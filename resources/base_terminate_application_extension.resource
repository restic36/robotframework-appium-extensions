*** Settings ***

Library     AppiumLibrary
Library    ../src/robotframework_appium_extensions/keywords/TerminateApplicationExtension.py

*** Variables ***
${REMOTE_URL}           http://localhost:4723
${PLATFORM_NAME}        Android
${PLATFORM_VERSION}     15
${DEVICE_NAME}          H6JVGU5HCY45CIT8
#${DEVICE_NAME}          emulator-5554
${AUTOMATION_NAME}      UiAutomator2
${MAX_SWIPE_RANGE}      1000
${MIN_SWIPE_RANGE}      1

*** Keywords ***
Start Session Youtube
    [Documentation]    Starts a new Appium session for the YouTube application
    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    deviceName=${DEVICE_NAME}
    ...    platformVersion=${PLATFORM_VERSION}
    ...    appPackage=com.google.android.youtube
    #      For use with xiaomi youtube app uncomment the line below
    ...    appActivity=com.google.android.youtube/.app.honeycomb.Shell$HomeActivity
    #      For use with emulator youtube app uncomment the line below
    # ...  appActivity=com.google.android.youtube.HomeActivity
    ...    automationName=${AUTOMATION_NAME}
    ...    noReset=true

Start Session TikTok
    [Documentation]    Starts a new Appium session for the TikTok application
    Open Application    ${REMOTE_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    deviceName=${DEVICE_NAME}
    ...    platformVersion=${PLATFORM_VERSION}
    ...    appPackage=com.zhiliaoapp.musically
    ...    appActivity=com.zhiliaoapp.musically/com.ss.android.ugc.aweme.splash.SplashActivity
    ...    automationName=${AUTOMATION_NAME}
    ...    noReset=true

Swipe Loop
    [Documentation]    Performs vertical swipes according to the specified range.
    ...                
    ...                Arguments:
    ...                - swipe_range: Number of swipes to perform (must be between ${MIN_SWIPE_RANGE} and ${MAX_SWIPE_RANGE})
    ...                
    ...                Example:
    ...                | Swipe Loop | 10 |
    [Arguments]    ${swipe_range}
    
    # Validate swipe_range parameter
    ${swipe_range_str}=    Convert To String    ${swipe_range}
    Run Keyword If    '${swipe_range_str}' == '${EMPTY}'
    ...    Fail    swipe_range parameter cannot be empty
    
    # Convert to integer and validate
    ${swipe_range_int}=    Run Keyword And Return Status    Convert To Integer    ${swipe_range}
    Run Keyword If    not ${swipe_range_int}
    ...    Fail    swipe_range must be a valid integer, got: ${swipe_range}
    
    ${swipe_range}=    Convert To Integer    ${swipe_range}
    
    # Validate range limits
    Run Keyword If    ${swipe_range} < ${MIN_SWIPE_RANGE}
    ...    Fail    swipe_range must be at least ${MIN_SWIPE_RANGE}, got: ${swipe_range}
    
    Run Keyword If    ${swipe_range} > ${MAX_SWIPE_RANGE}
    ...    Fail    swipe_range cannot exceed ${MAX_SWIPE_RANGE}, got: ${swipe_range}
    
    # Get screen dimensions
    ${x}           Get Window Width
    ${y}           Get Window Height
    ${start_x}     Evaluate    ${x} / 2
    ${start_y}     Evaluate    ${y} / 2
    ${end_y}       Evaluate    ${start_y} - (${y} * 0.4)

    Log    Starting swipe loop: ${swipe_range} swipes    level=INFO
    
    FOR    ${index}    IN RANGE    ${swipe_range}
        ${current}=    Evaluate    ${index} + 1
        Log    Performing swipe ${current} of ${swipe_range}    level=INFO
        Swipe
        ...    start_x=${start_x}
        ...    start_y=${start_y}
        ...    offset_x=${start_x}
        ...    offset_y=${end_y}
        Sleep    0.5s
    END
    
    Log    Completed ${swipe_range} swipes successfully    level=INFO