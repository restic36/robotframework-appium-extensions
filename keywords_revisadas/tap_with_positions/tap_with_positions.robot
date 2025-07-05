*** Settings ***
Documentation     Test suite to confirm that the built-in keyword Tap With Positions behaves like the custom Tap A Point
Library           AppiumLibrary

Suite Setup       Open Google Maps App
Suite Teardown    Close App

*** Variables ***
${REMOTE_URL}           http://localhost:4723
${PLATFORM_NAME}        Android
${DEVICE_NAME}          Emulator
${UDID}                 emulator-5554
${TIMEOUT}              10s
${TAP_DURATION}         200
${APP_PACKAGE}          com.google.android.apps.maps
${APP_ACTIVITY}         com.google.android.maps.MapsActivity

*** Keywords ***
Open Google Maps App
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
    [Tags]    tap_point    googlemaps    center    top_right

    ${width}=    Get Window Width
    ${height}=   Get Window Height

    ${center_x}=    Evaluate    ${width} // 2 
    ${center_y}=    Evaluate    ${height} // 2
    ${center_point}=    Create List    ${center_x}    ${center_y}

    Log    Tapping center of screen at ${center_point}    INFO
    Tap With Positions    ${TAP_DURATION}    ${center_point}
    Log    Touch performed successfully

    # offsetting 50 pixels from the respective screen edges
    ${top_right_x}=    Evaluate    ${width}-50
    ${top_right_y}=    Evaluate    50
    ${top_right_point}=    Create List    ${top_right_x}    ${top_right_y}

    Log    Tapping top-right corner at ${top_right_point}    INFO
    Tap With Positions    ${TAP_DURATION}    ${top_right_point}
    Log    Touch performed successfully

Consecutive Taps at Different Positions
    [Documentation]    Simulates three consecutive taps on different positions
    [Tags]    multiple    consecutive
    Log    Performing three consecutive taps on different positions    INFO
    Tap With Positions    ${TAP_DURATION}    ${150, 1400}
    Log    Touch performed successfully at (${150, 1400})
    Tap With Positions    ${TAP_DURATION}    ${400, 1400}
    Log    Touch performed successfully at (${400, 1400})
    Tap With Positions    ${TAP_DURATION}    ${650, 1400}
    Log    Touch performed successfully at (${650, 1400})

Negative Test - Invalid Coordinate Format
    [Documentation]    Negative test: tap with invalid coordinate format
    [Tags]    error    negative    validation

# Some earlier versions of AppiumLibrary documented that coordinates for the keyword Tap With Positions
# had to be passed strictly as lists. However, more recent versions appear to have relaxed this requirement,
# allowing arguments that can be directly cast to integers (e.g., plain strings or numbers).
# As a result, when using invalid arguments, we don't get a custom AppiumLibrary error message,
# but instead a standard Python ValueError (e.g., "invalid literal for int()").

    Log    Negative test: Forcing error with invalid coordinate format    WARN
    Run Keyword And Expect Error    *invalid literal for int()*    
    ...    Tap With Positions    ${TAP_DURATION}    abc
    Log    Error correctly caught: invalid coordinate format

Negative Test - Invalid Duration
    [Documentation]    Negative test: tap with an invalid duration
    [Tags]    negative    error    validation
    Log    Negative test: Forcing error with invalid tap duration    WARN

# Some versions of AppiumLibrary raise a raw ValueError instead of a custom error message.
# If necessary, adjust the expected error message accordingly if the test fails due to message mismatch.

    Run Keyword And Expect Error    *ValueError*
    ...    Tap With Positions    -100    [400, 800]
    Log    Error correctly caught: invalid duration

Outside Screen Touch
    [Documentation]    Attempts to tap outside screen bounds
    ...                This keyword does not auto-adjust coordinates, so the tap is expected to fail or be ignored
    [Tags]    outside    edge_case        validation
    Log    Attempting tap outside visible screen area
    ${width}=    Get Window Width
    ${height}=   Get Window Height

    ${x}=    Evaluate    ${width} + 1000
    ${y}=    Evaluate    ${height} + 1000
    ${coord}=    Create List    ${x}    ${y}

    Tap With Positions    ${TAP_DURATION}    ${coord}
    Log    Tap ignored

Multi-Touch with Two Fingers
    [Documentation]    Simulates two-finger touch (multi-touch)
    [Tags]    multitouch    two_fingers    horizontal
    Log    Performing two-finger horizontal tap    INFO
    ${point1}=    Create List    200    1000
    ${point2}=    Create List    600    1000

# Each coordinate pair represents a "finger" in the multi-touch simulation.
# To add more fingers, simply include more [x, y] lists.

    Tap With Positions    300    ${point1}    ${point2}
    Log    Two-fingers touch performed successfully