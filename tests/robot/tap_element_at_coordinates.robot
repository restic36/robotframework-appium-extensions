*** Settings ***
Library           AppiumLibrary
Library    ../src/robotframework_appium_extensions/keywords/TapElementAtCoordinates.py
Resource    ../../resources/base_tap_element_at_coordinates.resource

*** Test Cases ***
# Clicks at the center of the 'Camera' element (50% width and 50% height)
Click Camera At Center
    [Tags]    camera
    Start session
    Wait Until Element Is Visible    xpath=//android.widget.TextView[@content-desc="Camera"]    5s
    Tap Element At Coordinates    xpath=//android.widget.TextView[@content-desc="Camera"]    0.5    0.5
    Close session

# Clicks at the top left corner of the 'Camera' element (0% width, 0% height)
Click Camera At Top Left
    [Tags]    camera    position
    Start session
    Wait Until Element Is Visible    xpath=//android.widget.TextView[@content-desc="Camera"]    5s
    Tap Element At Coordinates    xpath=//android.widget.TextView[@content-desc="Camera"]    0    0
    Close session

# Clicks 10px from the left and 20px from the top of the 'Camera' element
Click Camera At Absolute Offset
    [Tags]    camera    offset
    Start session
    Wait Until Element Is Visible    xpath=//android.widget.TextView[@content-desc="Camera"]    5s
    Tap Element At Coordinates    xpath=//android.widget.TextView[@content-desc="Camera"]    10    20
    Close session

# Clicks at the center of calculator button 8 (50% width and height)
Click Calculator Button 8 At Center
    [Tags]    calculator
    Start session 1
    Wait Until Element Is Visible    id=com.google.android.calculator:id/digit_8    5s
    Tap Element At Coordinates    id=com.google.android.calculator:id/digit_8    0.5    0.5
    Close session

# Tests error for element not found
ClickC Element Not Found - Fixed
    [Tags]    error    locator
    Start session
    Run Keyword And Expect Error    ValueError: Element with locator*    Tap Element At Coordinates    xpath=//android.widget.TextView[@content-desc="NaoExiste"]    10    20
    Close session

# Tests error for coordinates out of bounds
ClickC Coordinates Out Of Bounds - Fixed
    [Tags]    error    coordinates
    Start session
    Wait Until Element Is Visible    xpath=//android.widget.TextView[@content-desc="Camera"]    5s
    Run Keyword And Expect Error    ValueError: Coordinates*out of device screen bounds*    Tap Element At Coordinates    xpath=//android.widget.TextView[@content-desc="Camera"]    200    200
    Close session

# Tests error for invalid parameter type
ClickC Invalid Offset Type - Fixed
    [Tags]    error    parameter
    Start session 1
    Wait Until Element Is Visible    id=com.google.android.calculator:id/digit_8    5s
    Run Keyword And Expect Error    ValueError: xoffset and yoffset must be numbers*    Tap Element At Coordinates    id=com.google.android.calculator:id/digit_8    abc    def
    Close session