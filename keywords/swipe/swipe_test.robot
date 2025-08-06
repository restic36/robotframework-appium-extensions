*** Settings ***
Resource    base_swipe.resource
Resource    elementos.resource

*** Test Cases ***
Deve realizar swipe no Rgb
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
