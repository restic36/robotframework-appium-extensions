*** Settings ***
Library    AppiumLibrary
Library    ./ChangeTheme.py
Library    Collections
Library    BuiltIn

*** Variables ***
${APPIUM_URL}         http://localhost:4723
${PLATFORM_NAME}      Android
${DEVICE_NAME}        XiaomiDevice
${UDID}               a83af8e7
${AUTOMATION_NAME}    UiAutomator2
${APP_PACKAGE}        com.miui.home
${APP_ACTIVITY}       .launcher.Launcher
${THEME_CHANGE_DELAY}   3


*** Keywords ***
Setup Test Environment
    [Documentation]    Configura ambiente de teste inicial
    Open Application  ${APPIUM_URL}
    ...    platformName=${PLATFORM_NAME}
    ...    deviceName=${DEVICE_NAME}
    ...    udid=${UDID}
    ...    automationName=${AUTOMATION_NAME}
    ...    appPackage=${APP_PACKAGE}
    ...    appActivity=${APP_ACTIVITY}
    ...    noReset=true
    Set Device UDID    ${UDID}
    Sleep    2s
   
Teardown Test Environment
    [Documentation]    Limpa ambiente após teste
    Close Application

Verify Theme Change
    [Documentation]    Verifica se o tema foi alterado corretamente
    [Arguments]    ${expected_theme}
    ${current_theme}=    Get Current Theme
    Should Be Equal As Strings    ${current_theme}    ${expected_theme}
    Log    Tema verificado: ${current_theme}

*** Test Cases ***
Muda Tema Para Escuro Via ADB
    [Documentation]    Testa a mudança do tema do dispositivo de claro para escuro usando ADB
    [Tags]    theme    dark_theme    adb    fast
    [Setup]    Setup Test Environment
    [Teardown]    Teardown Test Environment
    
    # Verifica tema inicial
    ${initial_theme}=    Get Current Theme
    Log    Tema inicial: ${initial_theme}
    
    # Muda para tema escuro
    Change To Dark Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    
    # Verifica se mudou corretamente
    Verify Theme Change    dark
    
    # Captura screenshot para evidência
    Capture Page Screenshot    dark_theme_applied.png

Muda Tema Para Claro Via ADB
    [Documentation]    Testa a mudança do tema do dispositivo de escuro para claro usando ADB
    [Tags]    theme    light_theme    adb    fast
    [Setup]    Setup Test Environment
    [Teardown]    Teardown Test Environment
    
    # Garante que está no tema escuro primeiro
    Change To Dark Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    
    # Verifica tema inicial
    ${initial_theme}=    Get Current Theme
    Log    Tema inicial: ${initial_theme}
    
    # Muda para tema claro
    Change To Light Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    
    # Verifica se mudou corretamente
    Verify Theme Change    light
    
    # Captura screenshot para evidência
    Capture Page Screenshot    light_theme_applied.png

Teste Alternância de Tema
    [Documentation]    Testa a alternância automática entre temas
    [Tags]    theme    toggle    adb    fast
    [Setup]    Setup Test Environment
    [Teardown]    Teardown Test Environment
    
    # Verifica tema inicial
    ${initial_theme}=    Get Current Theme
    Log    Tema inicial: ${initial_theme}
    
    # Alterna tema
    Toggle Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    
    # Verifica se alternou
    ${new_theme}=    Get Current Theme
    Should Not Be Equal As Strings    ${initial_theme}    ${new_theme}
    Log    Tema alternado de ${initial_theme} para ${new_theme}
    
    # Alterna novamente
    Toggle Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    
    # Verifica se voltou ao tema inicial
    ${final_theme}=    Get Current Theme
    Should Be Equal As Strings    ${initial_theme}    ${final_theme}
    Log    Tema retornado ao estado inicial: ${final_theme}

Teste Completo de Mudança de Tema
    [Documentation]    Teste completo que verifica todas as funcionalidades de tema
    [Tags]    theme    complete    adb    regression
    [Setup]    Setup Test Environment
    [Teardown]    Reset Theme To Auto
    
    # 1. Verifica tema inicial
    ${initial_theme}=    Get Current Theme
    Log    Tema inicial: ${initial_theme}
    
    # 2. Muda para escuro
    Change To Dark Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    Verify Theme Change    dark
    Capture Page Screenshot    step2_dark_theme.png
    
    # 3. Muda para claro
    Change To Light Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    Verify Theme Change    light
    Capture Page Screenshot    step3_light_theme.png
    
    # 4. Testa alternância
    Toggle Theme
    Sleep    ${THEME_CHANGE_DELAY}s
    Verify Theme Change    dark
    Capture Page Screenshot    step4_toggled_to_dark.png
    
    # 5. Reseta para automático
    Reset Theme To Auto
    Sleep    ${THEME_CHANGE_DELAY}s
    ${final_theme}=    Get Current Theme
    Should Be Equal As Strings    ${final_theme}    auto
    Log    Tema resetado para automático
    Capture Page Screenshot    step5_auto_theme.png

# Comparação com método original (comentado para não executar por padrão)
# Muda Tema Para Escuro em "Configurações" na Tela Inicial (Método Original)
#     [Documentation]    Testa a mudança do tema do dispositivo usando interface (método original)
#     [Tags]    theme    dark_theme    ui_automation    slow    original
#     [Setup]    Setup Test Environment
#     [Teardown]    Teardown Test Environment
#     
#     # Usa método original baseado em cliques (mais lento)
#     Change To Dark Theme    # Implementação original
#     Sleep    5s    # Método original precisa de mais tempo
#     
#     # Verifica resultado
#     ${current_theme}=    Get Current Theme
#     Should Be Equal As Strings    ${current_theme}    dark

   
    
