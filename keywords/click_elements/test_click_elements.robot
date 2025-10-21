*** Settings ***
Documentation    Test suite for multiple elements click functionality

Library     AppiumLibrary

Resource    ./base.resource

*** Test Cases ***
Should click multiple calculator buttons using ID locators
    [Tags]    calculator_id
    Start session Calculator
    
    # List using ID locators: 1, 2, 3
    @{elements}=    Create List
    ...    id=com.google.android.calculator:id/digit_1
    ...    id=com.google.android.calculator:id/digit_2
    ...    id=com.google.android.calculator:id/digit_3
    
    Click Elements    ${elements}    click_duration=200    interval_between_clicks=0.5
    
    Sleep    2
    Capture Page Screenshot
    Close session

Should click multiple calculator buttons using XPath locators
    [Tags]    calculator_xpath
    Start session Calculator
    
    # List using XPath locators: 4, 5, 6
    @{elements}=    Create List
    ...    xpath=//android.widget.ImageButton[@content-desc="4"]
    ...    xpath=//android.widget.ImageButton[@content-desc="5"]
    ...    xpath=//android.widget.ImageButton[@content-desc="6"]

    Click Elements    ${elements}    click_duration=250    interval_between_clicks=0.6

    Sleep    2
    Capture Page Screenshot
    Close session

Should click multiple calculator buttons using accessibility IDs
    [Tags]    calculator_accessibility
    Start session Calculator
    
    # List using accessibility IDs: 7, 8, 9
    @{elements}=    Create List
    ...    accessibility_id=7
    ...    accessibility_id=8
    ...    accessibility_id=9
    
    Click Elements    ${elements}    click_duration=300    interval_between_clicks=0.4
    
    Sleep    2
    Capture Page Screenshot
    Close session

Should perform calculation using mixed locator types
    [Tags]    mixed_locators_calculation
    Start session Calculator
    
    # Calculate: 2 + 3 = using mixed locators
    @{elements}=    Create List
    ...    id=com.google.android.calculator:id/digit_2
    ...    xpath=//android.widget.ImageButton[@content-desc="plus"]
    ...    accessibility_id=3
    ...    id=com.google.android.calculator:id/eq
    
    Click Elements    ${elements}    click_duration=200    interval_between_clicks=0.5
    
    Sleep    3
    Capture Page Screenshot
    Close session