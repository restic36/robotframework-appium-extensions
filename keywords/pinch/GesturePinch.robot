*** Settings ***

Resource    GesturePinchResource.robot

*** Test Cases ***

Pinch on Google Maps using a locator
    [Documentation]    Must perform Pinch on Google Maps application using a locator  
    [Tags]    maps
    Start session Google Maps
    Sleep    10    
    Perform Pinch Gesture    locator=xpath=//android.widget.ScrollView 
    Sleep    5

Pinch on Google Maps without a locator

    [Documentation]    Must perform Pinch on Google Maps without receiving a locator
    [Tags]    maps
    Start session Google Maps
    Sleep    10
    Perform Pinch Gesture
    Sleep    5