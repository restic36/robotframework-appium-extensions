*** Settings ***
Documentation    This test suite runs the applications and simulates their use by swiping upwards,
...              with the aim of testing the application's closure with the custom keyword terminate application
...              after prolonged use.
   
Library           AppiumLibrary
Resource          ./base.resource

*** Test Cases ***
Testar Encerramento do YouTube
    [Tags]    YouTube
    [Documentation]    Tests the termination of the YouTube application using the TerminateApplicationExtension
    ...                custom keyword after the "Shorts" video session and execution of several swipes.
    [Teardown]    Close Application
    Start Session Youtube
    Click Text    text=Shorts
    Swipe Loop    10
    ${app_id}=    Get Current App Id
    Log    Encerrando o aplicativo com ID: ${app_id}
    Terminate Application Extension        ${app_id}


Testar Encerramento do TikTok
    [Tags]    TikTok
    [Documentation]    Tests terminating the TikTok application using the TerminateApplicationExtension
    ...                custom keyword after executing multiple swipes.
    [Teardown]    Close Application
    Start Session TikTok
    Swipe Loop    10
    ${app_id}=    Get Current App Id
    Log    Encerrando o aplicativo com ID: ${app_id}
    Terminate Application Extension        ${app_id}