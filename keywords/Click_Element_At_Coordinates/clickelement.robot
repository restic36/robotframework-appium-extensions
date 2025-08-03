*** Settings ***
Library           AppiumLibrary

Resource          ./base.resource

*** Test Cases ***
Click Element At Center
    [tags]   android
    Start session
    
    Wait Until Element Is Visible    xpath=//android.widget.TextView[@content-desc="Camera"]    5s

    # Clique no centro do elemento usando porcentagem
    ClickC     xpath=//android.widget.TextView[@content-desc="Camera"]     0.5   0.5
    Close session

Click Element At Top Left
    [tags]   android
    Start session
    
    Wait Until Element Is Visible    xpath=//android.widget.TextView[@content-desc="Camera"]    5s

    # Clique no canto superior esquerdo do elemento
    ClickC     xpath=//android.widget.TextView[@content-desc="Camera"]     0   0
    Close session

Click Element At Specific Offset
    [tags]   android
    Start session
    
    Wait Until Element Is Visible    xpath=//android.widget.TextView[@content-desc="Camera"]    5s

    # Clique a 10px da esquerda e 20px do topo do elemento
    ClickC     xpath=//android.widget.TextView[@content-desc="Camera"]     10   20
    Close session

Click Element At Center
    [tags]   teste2
    Start session 1
    
    Wait Until Element Is Visible    id=com.google.android.calculator:id/digit_8   5s

    # Clique no centro do elemento usando porcentagem
    ClickC     id=com.google.android.calculator:id/digit_8    0.5   0.5
    Close session

