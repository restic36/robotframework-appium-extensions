*** Settings ***

Resource    GestureZoomResource.robot

*** Test Cases ***

Zoom on Google Maps using a locator
    [Documentation]    Must perform Zoom on Google Maps application using a locator  
    [Tags]    maps
    Start session Google Maps
    Sleep    10    
    Perform Zoom Gesture    locator=xpath=//android.widget.ScrollView 
    Sleep    5

Zoom on Google Maps without a locator

    [Documentation]    Must perform Zoom on Google Maps without receiving a locator
    [Tags]    maps
    Start session Google Maps
    Sleep    10
    Perform Zoom Gesture
    Sleep    5