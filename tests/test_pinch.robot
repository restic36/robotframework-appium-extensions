#-> principais sugestões:
# incluir suite setup e teardown, além da lista de variáveis pra parametrizar e facilitar o reuso
# alterar o url pro caminho WebDriver completo (com /wd/hub no final), garantindo uma compatibilidade mais ampla
# incluir um newCommandTimeout pra evitar quebra de teste por erro de sessão encerrada
# incluir PageScreenshot depois de cada teste pra fortalecer a documentação e ter uma evidência visual do gesto
#-> aqi nesse caso ele tá com um page screenshot depois de cada teste pra gente conseguir documemtar melhor o processo
#-> mas, se for o caso, podemos incluir um Run Keyword If Test Failed/Page Screenshot no Teardown pra não ficar repetitivo e não poluir o log
#-> tbm não tem incluso logs pra acompanhar a execução pra não poluir tanto, mas pode ser adicionado, caso necessário

*** Settings ***
Library    AppiumLibrary
Library    ../resources/GestureKeywords.py

Suite Setup       Abrir Aplicativo
Suite Teardown    Fechar Applicativo

*** Variables ***
${REMOTE_URL}     http://localhost:4723
${PLATFORM_NAME}  Android
${DEVICE_NAME}    Emulator
${UDID}           emulator-5554
${APP_PACKAGE}    com.google.android.apps.maps
${APP_ACTIVITY}   com.google.android.maps.MapsActivity
${TIMEOUT}        10s
#-> vamo usar um timeout de 10s pra evitar a quebra por elemtno não encontrado
#-> como o maps é um app com animação pesada, a gente pode usar 10 ou 15s

*** Keywords ***
Abrir Aplicativo
    Open Application    ${REMOTE_URL}    
    ...                 platformName=${PLATFORM_NAME}    
    ...                 deviceName=${DEVICE_NAME}
    ...                 appPackage=${APP_PACKAGE}    
    ...                 appActivity=${APP_ACTIVITY}
    ...                 udid=${UDID}
    ...                 autoGrantPermissions=true   
    ...                 automationName=UiAutomator2    
    ...                 newCommandTimeout=600

Fechar Applicativo
    Close Application

*** Test Cases ***
Pinch Vertical com Scale Médio
    [Documentation]    Executa gesto pinch vertical com scale médio em um elemento
    [Tags]    vertical    medium    googlemaps
    # vamo usar valores padrão de scale (que tbm é o valor médio), direction e movement e aumentar um pouco a duração
    Wait Until Element Is Visible    //android.widget.TextView[@text="Search here"]    ${TIMEOUT}
    #Log    Executando pinch vertical no mapa com scale de 0.5
    Perform Pinch Gesture    //android.widget.TextView[@text="Search here"]    scale=0.5    duration=100    direction=vertical    movement=200
    Sleep    5s
    Capture Page Screenshot 


# o robot nao  ta instanciando automaticamente a classe que eu criei no .py, ai nao ta vendo a keyword no teste
# tentei transformar a keyword em um modulo python criando uma pasta vazia de __init__.py dentro da pasta keywords - não funcionou
# conferi se o Robot não tava desatualizado ou corrompido - não funcionou
# adicionei a configuração do robot.pythonpath pra garantir que o VSCode sabe que a /keywords faz parte do pythonpath - não funcionou
# testei importar a biblioteca a partir da classe com "keywords.pinch.GestureKeywords" - não funcionou

# Pinch Horizontal com Scale Alto
#     [Documentation]    Executa gesto pinch horizontal com deslocamento forte
#     [Tags]    horizontal    high    googlemaps
#     # vamo usar um scale de 0.9 (gesto quase completo), pra testar deslocamento extremo
#     # vamo usar um locator diferente, pra garantir que a keyword funciona em multiplos contextos
#     Wait Until Element Is Visible    xpath=//android.view.View[@resource-id="com.google.android.apps.maps:id/main_map"]    ${TIMEOUT}
#     #Log    Executando pinch horizontal no mapa com scale de 0.9
#     Perform Pinch Gesture    xpath=//android.view.View[@resource-id="com.google.android.apps.maps:id/main_map"]    scale=0.9    duration=50    direction=horizontal    movement=200
#     Sleep    5s
#     Capture Page Screenshot

# Pinch com Elemento Não Encontrado
#     [Documentation]    Teste negativo: executar pinch em elemento inexistente
#     [Tags]    negative    error    not_found
#     # vamo forçar o erro (usando um locator inexistente) pra testar o sucesso da função e o tratamento de erro
#     #Log    Teste negativo: forçando erro ao tentar executar pinch em elemento inexistente    WARN
#     Run Keyword And Expect Error    Element not found*    Perform Pinch Gesture    xpath=//android.widget.ScrollView[@resource-id="Inexistente"]    scale=0.5    duration=100    direction=vertical    movement=200
#     #Log    Erro corretamente capturado: elemento não encontrado

# Pinch com Direção Inválida
#     [Documentation]    Teste negativo: executar pinch com uma direção Inválida
#     [Tags]    negative    error    googlemaps
#     # vamo tentar ou outro teste negativo, agora usando uma direção inválida
#     #Log    Teste negativo: forçando erro ao tentar usar uma direção inválida    WARN
#     Run Keyword And Expect Error    Value Error    Perform Pinch Gesture    xpath=//android.widget.ScrollView[@resource-id="com.google.android.apps.maps:id/explore_tab_home_bottom_sheet"]    scale=0.5    duration=50    direction=diagonal    movement=200
#     #Log    Erro corretamente capturado: direção inválida

# Pinch com Scale Mínimo
#     [Documentation]    Executa gesto com menor intensidade de movimento possível
#     [Tags]    minimum    vertical    googlemaps
#     Wait Until Element Is Visible    xpath=//android.widget.ScrollView[@resource-id="com.google.android.apps.maps:id/explore_tab_home_bottom_sheet"]    ${TIMEOUT}
#     #Log    Executando pinch vertical no mapa com scale mínimo
#     Perform Pinch Gesture     xpath=//android.widget.ScrollView[@resource-id="com.google.android.apps.maps:id/explore_tab_home_bottom_sheet"]    scale=0.1    duration=100    direction=vertical    movement=150
#     Sleep    5s
#     Capture Page Screenshot

# Pinch com Duração Longa
#     [Documentation]    Executa gesto com duração longa para simular movimento mais lento
#     [Tags]    slow    vertical    googlemaps
#     # vamo aumentar a duração pra 500
#     Wait Until Element Is Visible     xpath=//android.widget.ScrollView[@resource-id="com.google.android.apps.maps:id/explore_tab_home_bottom_sheet"]    ${TIMEOUT}
#     #Log    Executando pinch vertical no mapa com duração longa para simular movimento mais lento
#     Perform Pinch Gesture     xpath=//android.widget.ScrollView[@resource-id="com.google.android.apps.maps:id/explore_tab_home_bottom_sheet"]    scale=0.5    duration=500    direction=vertical    movement=200
#     Sleep    5s
#     Capture Page Screenshot
