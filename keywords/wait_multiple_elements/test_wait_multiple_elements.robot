*** Settings ***
Library    AppiumLibrary
Resource   ./base.resource

*** Test Cases ***
Should wait for multiple elements to become visible in the Play Store (all)
    [Tags]    wait_all_playstore
    Start Session Store

    @{locators}=    Create List
    ...    xpath=//androidx.compose.ui.platform.ComposeView[@resource-id="com.android.vending:id/0_resource_name_obfuscated"]/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View[1]
    ...    xpath=//androidx.compose.ui.platform.ComposeView[@resource-id="com.android.vending:id/0_resource_name_obfuscated"]/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[3]/android.view.View[5]/android.view.View
    ...    xpath=//android.widget.TextView[@text="Find fellow bookworms with Facebook Events. Connect with readers who get it."]  

    ${result}=    Wait Multiple Elements    ${locators}    timeout=15    wait_for_all=True
    Should Be True    ${result['xpath=//androidx.compose.ui.platform.ComposeView[@resource-id="com.android.vending:id/0_resource_name_obfuscated"]/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View[1]']}
    Should Be True    ${result['xpath=//androidx.compose.ui.platform.ComposeView[@resource-id="com.android.vending:id/0_resource_name_obfuscated"]/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[3]/android.view.View[5]/android.view.View']}
    Should Be True    ${result['xpath=//android.widget.TextView[@text="Find fellow bookworms with Facebook Events. Connect with readers who get it."]']}

    Close Session

Should wait for any visible element in the Play Store (any)
    [Tags]    wait_any_playstore
    Start Session Store

    @{locators}=    Create List
    ...    xpath=//android.widget.TextView[@text="Top charts"]
    ...    xpath=//elemento_inexistente

    ${result}=    Wait Multiple Elements    ${locators}    timeout=10    wait_for_all=False
    Should Be True    ${result['xpath=//android.widget.TextView[@text="Top charts"]']}
    Should Not Be True   ${result['xpath=//elemento_inexistente']}

    Close Session

Should fail if no element exists in the Play Store
    [Tags]    wait_none_playstore
    Start Session Store

    @{locators}=    Create List
    ...    xpath=//elemento_inexistente_1
    ...    xpath=//elemento_inexistente_2

    Run Keyword And Expect Error    *Timeout*    Wait Multiple Elements    ${locators}    timeout=5    wait_for_all=False

    Close Session

Should fail if not all elements exist in the Play Store (wait_for_all=True)
    [Tags]    wait_all_fail_playstore
    Start Session Store

    @{locators}=    Create List
    ...    xpath=//android.widget.TextView[@text="Top charts"]
    ...    xpath=//elemento_inexistente

    Run Keyword And Expect Error    *Timeout*    Wait Multiple Elements    ${locators}    timeout=5    wait_for_all=True

    Close Session