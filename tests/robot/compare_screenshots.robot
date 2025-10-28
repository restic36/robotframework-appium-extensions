*** Settings ***
Library     AppiumLibrary
Library    ../../src/robotframework_appium_extensions/keywords/TapElementAtCoordinates.py
Library    ../../src/robotframework_appium_extensions/keywords/CompareScreenshots.py
Resource    ../../resources/base_compare_screenshots.resource

*** Variables ***
${PATH}      ${EXECDIR}/tests/assets/compare screenshots

*** Test Cases ***

Compare Screen Without Changes
    [Tags]    success
    Create Directory    ${PATH}
    Start Session Google Maps
    Sleep   5s
    Capture Page Screenshot    filename=${PATH}/default.png
    Sleep    2s
    Capture Page Screenshot    filename=${PATH}/default_final.png
    Compare Screenshots    img1=${PATH}/default.png    img2=${PATH}/default_final.png    expected=Equal
    Close Application


Compare Screen After Zoom Out
    [Tags]    difference
    Create Directory    ${PATH}
    Start Session Google Maps
    Sleep   5s
    Capture Page Screenshot    filename=${PATH}/zoom.png
    Perform Pinch Gesture    id=com.google.android.apps.maps:id/mainmap_container
    Sleep    2s
    Capture Page Screenshot    filename=${PATH}/zoom_final.png
    Compare Screenshots    img1=${PATH}/zoom.png    img2=${PATH}/zoom_final.png    expected=Different
    Close Application


Compare Screen After Map Scroll
    [Tags]    difference
    Create Directory    ${PATH}
    Start Session Google Maps
    Sleep   5s
    Capture Page Screenshot    filename=${PATH}/scroll.png
    Swipe    500    800    200    800    1000
    Sleep    2s
    Capture Page Screenshot    filename=${PATH}/scroll_final.png
    Compare Screenshots    img1=${PATH}/scroll.png    img2=${PATH}/scroll_final.png    expected=Different
    Close Application


Compare Screen After Typing
    [Tags]    difference
    Create Directory    ${PATH}
    Start Session Google Maps
    Sleep   5s
    Capture Page Screenshot    filename=${PATH}/search.png
    Click Element    id=com.google.android.apps.maps:id/search_omnibox_text_box
    Input Text       id=com.google.android.apps.maps:id/search_omnibox_edit_text    Salvador
    Sleep    2s
    Capture Page Screenshot    filename=${PATH}/search_final.png
    Compare Screenshots    img1=${PATH}/search.png    img2=${PATH}/search_final.png    expected=Different
    Close Application

Compare Screen After inicio
    [Tags]    inicio
    Create Directory    ${PATH}
    Start Session
    Capture Page Screenshot    filename=${PATH}/search.png
    Sleep    2s
    Capture Page Screenshot    filename=${PATH}/search_final.png
    Compare Screenshots    img1=${PATH}/search.png    img2=${PATH}/search_final.png    expected=Different
    Close Application


Compare Screen Calculator    
    [Tags]    calculator
    Create Directory    ${PATH}
    Start session 1
    sleep     2s
    Capture Page Screenshot    filename=${PATH}/calc_before.png
    Sleep   2s
    Tap Element At Coordinates    id=com.google.android.calculator:id/digit_8
    Tap Element At Coordinates  id=com.google.android.calculator:id/op_add
    Tap Element At Coordinates    id=com.google.android.calculator:id/digit_6
    Tap Element At Coordinates  id=com.google.android.calculator:id/op_add
    Tap Element At Coordinates    id=com.google.android.calculator:id/digit_4
    Sleep   2s
    Capture Page Screenshot    filename=${PATH}/calc_after.png
    Compare Screenshots    img1=${PATH}/calc_before.png    img2=${PATH}/calc_after.png    expected=Different
    Close Application

