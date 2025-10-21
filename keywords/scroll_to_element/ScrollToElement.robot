*** Settings ***

Resource    ScrollToElement.resource
*** Test Cases ***

Finding an application icon on home screen by scrolling without using a container locator
    [Documentation]    Must find an Gmail application on home screen by scrolling without using a container locator
    [Tags]    scroll
    
    Open Home Screen
    Press Keycode    3
    Scroll To Element    locator=//android.widget.TextView[@content-desc="Gmail"]
    ...    max_swipes=5    swipe_distance_ratio=0.8    direction=right
    
    Wait Until Element Is Visible     //android.widget.TextView[@content-desc="Gmail"]

Finding an application icon on home screen by scrolling using a container locator
    [Documentation]    Must find an Gmail application on home screen by scrolling using a container locator
    [Tags]    scroll
    
    Open Home Screen
    Press Keycode    3
    Scroll To Element    container_locator=//android.widget.ScrollView[@resource-id="com.google.android.apps.nexuslauncher:id/workspace"]   locator=//android.widget.TextView[@content-desc="Gmail"]
    ...    max_swipes=5    swipe_distance_ratio=0.8    direction=right
    
    Wait Until Element Is Visible     //android.widget.TextView[@content-desc="Gmail"]

