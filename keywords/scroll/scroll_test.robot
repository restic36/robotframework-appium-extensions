*** Settings ***
Resource    base_scroll.resource
Resource    elementos.resource


*** Test Cases ***
Deve realizar scroll no Play Store
    [Tags]    scroll
    Start session Play Store
    Sleep    10
    Wait Until Element Is Visible    //androidx.compose.ui.platform.ComposeView[@resource-id="com.android.vending:id/0_resource_name_obfuscated"]/android.view.View/android.view.View[2]/android.view.View/android.view.View[2]/android.view.View[2]
    Sleep    10
    Scroll Inside
    ...    ${playStore_elemento_xpath}
    ...    direction=left
    ...    percent=0.70
    ...    speed=500
    Sleep    2 

Deve realizar scroll down no Timer
    [Tags]    scroll
    Start session Timer
    Sleep    10
    Wait Until Element Is Visible    //android.widget.TextView[@text="Timer"]
    Sleep    10
    Scroll Inside
    ...    ${timer_elemento_id}
    ...    direction=down
    ...    percent=0.6
    ...    speed=300
    Sleep    2