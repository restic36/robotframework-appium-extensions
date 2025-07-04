*** Settings ***
Documentation     Test suite for the custom keyword Tap A Point
Library           AppiumLibrary
Library           TapAPoint

Suite Setup       Open Calculator App
Suite Teardown    Close App

*** Variables ***
${REMOTE_URL}           http://localhost:4723
${PLATFORM_NAME}        Android
${DEVICE_NAME}          Emulator
${UDID}                 emulator-5554
${TIMEOUT}              10s
${TAP_DURATION}         200
${APP_PACKAGE}          com.google.android.calculator
${APP_ACTIVITY}         com.android.calculator2.Calculator

*** Keywords ***
Open Calculator App
    Open Application    ${REMOTE_URL}
    ...                 automationName=uiautomator2
    ...                 platformName=${PLATFORM_NAME}
    ...                 deviceName=${DEVICE_NAME}
    ...                 udid=${UDID}
    ...                 autoGrantPermissions=true
    ...                 appPackage=${APP_PACKAGE}
    ...                 appActivity=${APP_ACTIVITY}
    ...                 newCommandTimeout=600

Close App
    Close Application

*** Test Cases ***
Tap Center and Top-Right of Screen
    [Documentation]    Performs a tap in the center and another in the top-right corner of the screen
    [Tags]    tap_point    calculator
    ${width}=    Get Window Width
    ${height}=   Get Window Height

    ${center_x}=    Evaluate    ${width} // 2
    ${center_y}=    Evaluate    ${height} // 2
    Tap A Point    ${center_x}    ${center_y}    ${TAP_DURATION}
    Sleep    2
    Log    Touch performed successfully

    ${top_right_x}=    Evaluate    ${width} - 50
    ${top_right_y}=    Evaluate    50
    Tap A Point    ${top_right_x}    ${top_right_y}    ${TAP_DURATION}
    Sleep    2
    Log    Touch performed successfully

Consecutive Taps at Different Positions
    [Documentation]    Performs consecutive taps on calculator buttons 7, 8, and 9 
    [Tags]    multiple_taps    calculator
    Tap A Point    150    1400    ${TAP_DURATION}
    Element Text Should Be    com.google.android.calculator:id/formula    7    ${TIMEOUT}
    Log    Touch performed successfully
    Tap A Point    400    1400    ${TAP_DURATION}
    Element Text Should Be    com.google.android.calculator:id/formula    78    ${TIMEOUT}
    Log    Touch performed successfully
    Tap A Point    650    1400    ${TAP_DURATION}
    Element Text Should Be    com.google.android.calculator:id/formula    789    ${TIMEOUT}
    Log    Touch performed successfully

Negative Test - Invalid Coordinate
    [Documentation]    Negative test: perform tap with an invalid coordinate
    [Tags]    negative    error    validation
    Log    Negative test: forcing error by trying to use an invalid coordinate    WARN
    Run Keyword And Expect Error    *x* and *y* must be integers*    
    ...    Tap A Point    abc    200    ${TAP_DURATION}
    Log    Error correctly caught: invalid coordinate

Negative Test - Invalid Duration
    [Documentation]    Negative test: perform tap with an invalid duration
    [Tags]    negative    error    validation
    Log    Negative test: forcing error by trying to use an invalid duration    WARN
    Run Keyword And Expect Error    *duration* must be a positive integer*
    ...    Tap A Point    300    800    -100
    Log    Error correctly caught: invalid duration

Negative Test - Malformed List
    [Documentation]    Negative test: perform tap with an unexpected argument type
    [Tags]    negative    error    structure
    Comment    This keyword does not support list input directly — simulating error with unexpected type
    Log    Negative test: forcing error by passing a list as an argument    WARN
    Run Keyword And Expect Error    *must be integers*    
    ...    Tap A Point    [300, 800]    100

Outside Screen Touch
    [Documentation]    Perform tap on off-screen coordinates and checks if coordinates are adjusted
    [Tags]    outside    edge_case    adjusted        validation
    Log    Forcing adjust by trying to use an off-screen coordinate
    ${width}=    Get Window Width
    ${height}=   Get Window Height

    ${x}=    Evaluate    ${width} + 1000
    ${y}=    Evaluate    ${height} + 1000

    Tap A Point    ${x}    ${y}    ${TAP_DURATION}
    Log    Coordinates adjusted to screen bounds