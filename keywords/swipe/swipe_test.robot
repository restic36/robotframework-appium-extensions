*** Settings ***
Resource    base_swipe.resource
Resource    elementos.resource

*** Test Cases ***
Should swipe on RGB
    [Tags]    swipe
    Start session Rgb
    Sleep    10
    Wait Until Element Is Visible    //android.widget.TextView[@text="RGB Picker de cores"]
    Sleep    5
    Swipe Element
    ...    ${rgb_elemento_xpath}
    ...    direction=right
    ...    percent=1
    ...    speed=500
    Sleep    2
    Swipe Element
    ...    ${rgb_elemento_id}
    ...    direction=right
    ...    percent=0.75
    ...    speed=500
    Sleep    2
Should swipe down on Timer
    [Tags]    swipe
    Start session Timer
    Sleep    10
    Wait Until Element Is Visible    //android.widget.TextView[@text="Timer"]
    Sleep    10
    Swipe Element
    ...    ${timer_elemento_id}
    ...    direction=up
    ...    percent=0.8
    ...    speed=500
    Sleep    2

# TEST FOR ERROR RETURN  (Element locator '//android.widget.TextView[@text="imer"]' did not match any elements)
Should swipe down on Timer with error
    [Tags]    swipe
    Start session Timer
    Sleep    10
    Wait Until Element Is Visible    //android.widget.TextView[@text="imer"]
    Sleep    10
    Swipe Element
    ...    ${timer_elemento_id}
    ...    direction=up
    ...    percent=0.8
    ...    speed=500
    Sleep    2
