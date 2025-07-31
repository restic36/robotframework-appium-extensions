*** Settings ***

Resource    base_fisico.resource

*** Test Cases ***

Deve encontrar o elemento selecionado
    [Tags]    notes
    Start session Samsung Notes
    Wait Until Page Contains Element    //android.widget.ImageView[@content-desc="Todas as notas"]
    Click Element    //android.widget.ImageView[@content-desc="Todas as notas"]
    Wait Until Page Contains Element    //android.widget.TextView[@text="Todas as notas"]
    Swipe To Element    //android.widget.TextView[@resource-id="com.samsung.android.app.notes:id/title" and @text="‎Sol_Ingenieria_Mecanica_ESTATICA_R_C_Hib"]    
    ...    max_swipes=100    direction=up
    Capture Page Screenshot
    Sleep    5
    Swipe To Element    container_locator=//android.widget.GridView[@resource-id="com.samsung.android.app.notes:id/noteslist_recyclerview"]
    ...    locator=//android.widget.TextView[@resource-id="com.samsung.android.app.notes:id/title" and @text="‎toaz.info-petroleo-e-seus-derivados-marco-antonio-"]
    ...    max_swipes=100    direction=down    swipe_distance_ratio=0.8
    Capture Page Screenshot

Deve encontrar o ano selecionado
    [Tags]    calendario

    Start session Calendario
    Wait Until Page Contains Element    //android.widget.RelativeLayout[@content-desc="Exibição anual, Botão"]
    Click Element    //android.widget.RelativeLayout[@content-desc="Exibição anual, Botão"]
    
    Swipe To Element    container_locator=com.samsung.android.calendar:id/year_pager
    ...    locator=//android.widget.TextView[@content-desc="2029, Toque duas vezes para alterar o ano."]
    ...    max_swipes=10    direction=left    swipe_distance_ratio=0.8
    
    Swipe To Element    container_locator=com.samsung.android.calendar:id/year_pager
    ...    locator=//android.widget.TextView[@content-desc="2025, Toque duas vezes para alterar o ano."]
    ...    max_swipes=5    direction=right    swipe_distance_ratio=0.8


Deve encontrar o elemento de formatação no Google Docs partindo da Tela Inicial
    [Tags]    docs
    
    Start session Tela Inicial
    Press Keycode    3
    Swipe To Element    locator=//android.widget.TextView[@content-desc="Teste SwipeIntoElement"]
    ...    max_swipes=5    swipe_distance_ratio=0.8    direction=right
    
    Click Element    //android.widget.TextView[@content-desc="Teste SwipeIntoElement"]
    
    Wait Until Element Is Visible    //android.widget.CompoundButton[@content-desc="Formatar"]    5
    Click Element    //android.widget.CompoundButton[@content-desc="Formatar"]
    
    Wait Until Element Is Visible    //android.widget.LinearLayout[@resource-id="com.google.android.apps.docs.editors.docs:id/btn_show_font_family"]
    
    Swipe To Element    locator=//android.widget.Button[@resource-id="com.google.android.apps.docs.editors.docs:id/btn_clear_formatting"]
    ...    container_locator=//android.widget.LinearLayout[@resource-id="com.google.android.apps.docs.editors.docs:id/formatting_fragment_sections_view"]
    ...    max_swipes=5    swipe_distance_ratio=0.2    direction=up 




