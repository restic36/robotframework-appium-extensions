*** Settings ***

Library     AppiumLibrary

Resource    base.resource



*** Test Cases ***
Teste de clique longo pressionando um icone
    [Tags]        inicio
    
    Start session


    LongP        xpath=//android.widget.TextView[@content-desc="Gmail"]     8000
    Capture Page Screenshot


 
Teste de clique longo com calculadora
        [Tags]    calculadora

    Start session 1


    LongP     id=com.google.android.calculator:id/digit_8     8000
    Capture Page Screenshot


    Close session

Teste de clique longo
    [Tags]                      long

    Start session 2
    Get started
    Navigate to                 Clique em Botões
    Go to item                  Clique longo                               Botão clique longo

    LongP                     id=com.qaxperience.yodapp:id/long_click    

    Wait Until Page Contains    Isso é um clique longo
    Capture Page Screenshot

    Close session
Botão inexistente não deve estar presente
    [Tags]    erro_esperado
    Start session 
    Element Should Be Visible    xpath=//android.widget.Button[@text="Inexistente"]
    Capture Page Screenshot

    Close session

App YouTube não deve estar presente na tela inicial
    [Tags]        elemento_ausente   
    Start session 
    Page Should Not Contain Element   xpath=//android.widget.TextView[@content-desc="YouTube"]
    Close session

    
Erro esperado ao usar LongP em elemento ausente
    [Tags]    erro1_esperado    Start session 2

    ${erro}=    Set Variable    Nenhum erro

    TRY
        LongP    id=botao_inexistente    8000
    EXCEPT    ${erro}
        ${linha_erro}=    Evaluate    str($erro).splitlines()[0]
        Log    ${linha_erro}
    END

    Capture Page Screenshot
    Close session



Erro esperado ao usar LongP com locator inválido
    [Tags]    erro2_esperado
    Start session 

    Run Keyword And Expect Error     Invalid locator syntax
    ...    LongP    invalid-locator    8000

    Capture Page Screenshot
    Close session

Erro esperado ao usar LongP sem duração
    [Tags]    erro3_esperado
    Start session 

    Run Keyword And Expect Error     Missing required argument 'duration'
    ...    LongP    id=com.qaxperience.yodapp:id/long_click

    Capture Page Screenshot
    Close session

Erro esperado ao usar LongP em elemento não suportado
    [Tags]    erro4_esperado
    Start session 

    Run Keyword And Expect Error     Element does not support long press
    ...    LongP    id=com.qaxperience.yodapp:id/unsupported_element    8000

    Capture Page Screenshot
    Close session
