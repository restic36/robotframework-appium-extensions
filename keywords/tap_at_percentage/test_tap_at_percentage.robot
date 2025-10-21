*** Settings ***
Library    AppiumLibrary
Library    ./TapAtPercentage.py    
Resource   ./base.resource

*** Test Cases ***
Should tap at number 0 successfully
    [Tags]    tap_zero
    Start Session Calculator
    Tap At Percentage    x=0.1    y=0.9    duration=200
    Element Should Contain Text    locator=xpath=//android.widget.EditText[@resource-id="com.google.android.calculator:id/formula"]    expected=0
    Close Session

Should tap at number 5 successfully
    [Tags]    tap_five
    Start Session Calculator
    Tap At Percentage    x=0.4    y=0.7    duration=200
    Element Should Contain Text    locator=xpath=//android.widget.EditText[@resource-id="com.google.android.calculator:id/formula"]    expected=5
    Close Session

Should tap at More Options button successfully
    [Tags]    tap_more_options
    Start Session Calculator
    Tap At Percentage    x=0.95    y=0.05    duration=100
    Text Should Be Visible    Help
    Close Session

Should fail with invalid x coordinate (greater than 1)
    [Tags]    validation_fail
    Start Session Calculator
    Run Keyword And Expect Error    *percentages between 0.0 and 1.0*
    ...    Tap At Percentage    x=1.5    y=0.5    duration=100
    Close Session

Should fail with invalid y coordinate (negative)
    [Tags]    validation_fail
    Start Session Calculator
    Run Keyword And Expect Error    *percentages between 0.0 and 1.0*
    ...    Tap At Percentage    x=0.5    y=-0.1    duration=100
    Close Session

Should fail with non-numeric x coordinate
    [Tags]    validation_fail
    Start Session Calculator
    Run Keyword And Expect Error    *must be numbers (float)*
    ...    Tap At Percentage    x=abc    y=0.5    duration=100
    Close Session

Should fail with non-numeric y coordinate
    [Tags]    validation_fail
    Start Session Calculator
    Run Keyword And Expect Error    *must be numbers (float)*
    ...    Tap At Percentage    x=0.5    y=xyz    duration=100
    Close Session

Should fail with negative duration
    [Tags]    validation_fail
    Start Session Calculator
    Run Keyword And Expect Error    *must be a positive integer*
    ...    Tap At Percentage    x=0.5    y=0.5    duration=-100
    Close Session

Should fail with zero duration
    [Tags]    validation_fail
    Start Session Calculator
    Run Keyword And Expect Error    *must be a positive integer*
    ...    Tap At Percentage    x=0.5    y=0.5    duration=0
    Close Session

Should fail with string duration
    [Tags]    validation_fail
    Start Session Calculator
    Run Keyword And Expect Error    *must be a positive integer*
    ...    Tap At Percentage    x=0.5    y=0.5    duration=abc
    Close Session

Should work with boundary values
    [Tags]    boundary_test
    Start Session Calculator
    # Test exact boundary values
    Tap At Percentage    x=0.0    y=0.0    duration=50
    Sleep    0.5s
    Tap At Percentage    x=1.0    y=1.0    duration=50
    Sleep    0.5s
    Tap At Percentage    x=0.0    y=1.0    duration=50
    Sleep    0.5s
    Tap At Percentage    x=1.0    y=0.0    duration=50
    Close Session

Should work with decimal coordinates
    [Tags]    decimal_test
    Start Session Calculator
    Tap At Percentage    x=0.33    y=0.66    duration=100
    Sleep    0.5s
    Tap At Percentage    x=0.789    y=0.123    duration=100
    Sleep    0.5s
    Tap At Percentage    x=0.001    y=0.999    duration=100
    Close Session

Should handle multiple rapid taps
    [Tags]    rapid_taps
    Start Session Calculator
    FOR    ${i}    IN RANGE    5
        Tap At Percentage    x=0.5    y=0.5    duration=50
        Sleep    0.2s
    END