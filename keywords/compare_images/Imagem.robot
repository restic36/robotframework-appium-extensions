*** Settings ***
Library     AppiumLibrary
Resource    ./base.resource


*** Variables ***
${PATH}      screenshots

*** Test Cases ***

Compare Screen Without Changes
    [Tags]    success
    Start Session Google Maps
    sleep   5s
    Capture Initial Screenshot As    default.png    ${PATH}
    Sleep    2s
    Compare Final Screenshot With    ${PATH}/default.png    0.15    ${PATH}
    Close Application

Compare Screen After Zoom Out
    [Tags]    difference
    Start Session Google Maps
    sleep   5s
    Capture Initial Screenshot As    zoom.png    ${PATH}
    Perform Pinch Gesture    id=com.google.android.apps.maps:id/mainmap_container
    Sleep    2s
    Compare Final Screenshot With    ${PATH}/zoom.png    0.15    ${PATH}
    Close Application

Compare Screen After Map Scroll
    [Tags]    difference
    Start Session Google Maps
    sleep   5s
    Capture Initial Screenshot As    scroll.png    ${PATH}
    Swipe    500    800    200    800    1000
    Sleep    2s
    Compare Final Screenshot With    ${PATH}/scroll.png    0.15    ${PATH}
    Close Application

Compare Screen After Typing
    [Tags]    difference
    Start Session Google Maps
    sleep   5s
    Capture Initial Screenshot As    search.png    ${PATH}
    Click Element    id=com.google.android.apps.maps:id/search_omnibox_text_box
    Input Text       id=com.google.android.apps.maps:id/search_omnibox_edit_text    Salvador
    Sleep    2s
    Compare Final Screenshot With    ${PATH}/search.png    0.15    ${PATH}
    Close Application

Compare Screen After Long Press
    [Tags]   long_press
    Start Session 
    Capture Initial Screenshot As    longpress.png    ${PATH}
    LongP    xpath=//android.widget.TextView[@content-desc="Gmail"]     8000
    Sleep    2s
    Compare Final Screenshot With    ${PATH}/longpress.png    0.15    ${PATH}
    Close Application

Compare Screen
    [Tags]   screen
    Start Session 
    Capture Initial Screenshot As    longpress.png    ${PATH}
   # LongP    xpath=//android.widget.TextView[@content-desc="Gmail"]     8000
    Sleep    2s
    Compare Final Screenshot With    ${PATH}/longpress.png    0.15    ${PATH}
    Close Application