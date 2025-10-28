*** Settings ***
Documentation    This test suite runs the applications and simulates their use by swiping upwards,
...              with the aim of testing the application's closure with the custom keyword terminate application
...              after prolonged use. We use YouTube and TikTok as examples because both applications
...              feature the swipe-up interaction as a primary form of navigation and content consumption
   
Library           AppiumLibrary
Resource    ../../resources/base_terminate_application_extension.resource

*** Test Cases ***
Test YouTube Application Termination
    [Tags]    YouTube    Positive
    [Documentation]    Tests the termination of the YouTube application using the TerminateApplicationExtension
    ...                custom keyword after the "Shorts" video session and execution of several swipes.
    [Teardown]    Close Application
    Start Session Youtube
    Wait Until Element Is Visible    accessibility_id=Shorts    5s
    Click Element    accessibility_id=Shorts

    Swipe Loop    10
    ${app_id}=    Get Current App Id
    Log    Terminating application with ID: ${app_id}    level=INFO
    Terminate Application Extension    ${app_id}


Test TikTok Application Termination
    [Tags]    TikTok    Positive
    [Documentation]    Tests terminating the TikTok application using the TerminateApplicationExtension
    ...                custom keyword after executing multiple swipes.
    [Teardown]    Close Application
    Start Session TikTok
    Swipe Loop    10
    ${app_id}=    Get Current App Id
    Log    Terminating application with ID: ${app_id}    level=INFO
    Terminate Application Extension    ${app_id}


Test Terminate Non-Existent Application
    [Tags]    Negative    TerminateFail
    [Documentation]    Verifies that attempting to terminate an application with an invalid ID fails with appropriate error.
    ...                Expected error: Application not installed on device
    [Teardown]    Close Application
    Start Session Youtube
    ${app_id}=    Set Variable    com.app.nonexistent
    Log    Attempting to terminate non-existent application: ${app_id}    level=INFO
    Run Keyword And Expect Error    *not installed*    Terminate Application Extension    ${app_id}


Test Terminate With Empty App ID
    [Tags]    Negative    TerminateFail    Validation
    [Documentation]    Verifies that attempting to terminate with empty app_id fails with validation error.
    ...                Expected error: app_id parameter cannot be empty
    [Teardown]    Close Application
    Start Session Youtube
    ${app_id}=    Set Variable    ${EMPTY}
    Log    Attempting to terminate with empty app_id    level=INFO
    Run Keyword And Expect Error    *cannot be empty*    Terminate Application Extension    ${app_id}


Test Terminate With Invalid App ID Format
    [Tags]    Negative    TerminateFail    Validation
    [Documentation]    Verifies that attempting to terminate with invalid app_id format fails.
    ...                Expected error: Invalid app_id format
    [Teardown]    Close Application
    Start Session Youtube
    ${app_id}=    Set Variable    invalid_app_id
    Log    Attempting to terminate with invalid app_id format: ${app_id}    level=INFO
    Run Keyword And Expect Error    *Invalid app_id format*    Terminate Application Extension    ${app_id}


Test Swipe Loop With Invalid Range - Negative
    [Tags]    Negative    SwipeFail    Validation
    [Documentation]    Verifies that Swipe Loop fails when given a negative number.
    ...                Expected error: swipe_range must be at least 1
    [Teardown]    Close Application
    Start Session Youtube
    Log    Attempting swipe with negative range: -5    level=INFO
    Run Keyword And Expect Error    *must be at least*    Swipe Loop    -5


Test Swipe Loop With Zero Range
    [Tags]    Negative    SwipeFail    Validation
    [Documentation]    Verifies that Swipe Loop fails when given zero as range.
    ...                Expected error: swipe_range must be at least 1
    [Teardown]    Close Application
    Start Session Youtube
    Log    Attempting swipe with zero range    level=INFO
    Run Keyword And Expect Error    *must be at least*    Swipe Loop    0


Test Swipe Loop With Excessive Range
    [Tags]    Negative    SwipeFail    Validation
    [Documentation]    Verifies that Swipe Loop fails when given a range exceeding maximum limit.
    ...                Expected error: swipe_range cannot exceed maximum
    [Teardown]    Close Application
    Start Session Youtube
    ${excessive_range}=    Set Variable    10000
    Log    Attempting swipe with excessive range: ${excessive_range}    level=INFO
    Run Keyword And Expect Error    *cannot exceed*    Swipe Loop    ${excessive_range}


Test Swipe Loop With Non-Integer Value
    [Tags]    Negative    SwipeFail    Validation
    [Documentation]    Verifies that Swipe Loop fails when given a non-integer value.
    ...                Expected error: swipe_range must be a valid integer
    [Teardown]    Close Application
    Start Session Youtube
    Log    Attempting swipe with non-integer value: abc    level=INFO
    Run Keyword And Expect Error    *must be a valid integer*    Swipe Loop    abc