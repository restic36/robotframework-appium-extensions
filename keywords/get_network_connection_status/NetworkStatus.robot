*** Settings ***
Resource    NetworkStatusResource.robot

Suite Setup       Initialize Appium Connection

*** Test Cases ***

# Mocked test case using an unknown bitmask to trigger the UNKNOWN status return

Wi-Fi Only Connection
    [Documentation]    Should return WIFI_ONLY when only Wi-Fi is enabled.
    [Tags]    wifi
    ${status}=    Get Readable Network Status
    Log    Status returned: ${status}
    Should Be Equal    ${status}    WIFI_ONLY

Mobile Data Only Connection
    [Documentation]    Should return DATA_ONLY when only mobile data is enabled.
    [Tags]    data
    ${status}=    Get Readable Network Status
    Log    Status returned: ${status}
    Should Be Equal    ${status}    DATA_ONLY

Wi-Fi And Data Active
    [Documentation]    Should return WIFI_AND_DATA when both Wi-Fi and mobile data are enabled.
    [Tags]    combined
    ${status}=    Get Readable Network Status
    Log    Status returned: ${status}
    Should Be Equal    ${status}    WIFI_AND_DATA

Airplane Mode Active (Wi-Fi and Data Disabled)
    [Documentation]    Should return AIRPLANE_MODE when airplane mode is enabled and Wi-Fi and data are off.
    [Tags]    airplane_mode
    ${status}=    Get Readable Network Status
    Log    Status returned: ${status}
    Should Be Equal    ${status}    AIRPLANE_MODE

No Active Connection
    [Documentation]    Should return NONE when all connectivity options are off and airplane mode is also off.
    [Tags]    none
    ${status}=    Get Readable Network Status
    Log    Status returned: ${status}
    Should Be Equal    ${status}    NONE

Airplane Mode with Wi-Fi Enabled
    [Documentation]    Even if Wi-Fi is on, should return AIRPLANE_MODE if airplane mode is active.
    [Tags]    airplane_mode    conflict
    ${status}=    Get Readable Network Status
    Log    Status returned: ${status}
    Should Be Equal    ${status}    AIRPLANE_MODE

Airplane Mode with Mobile Data Enabled
    [Documentation]    Should return AIRPLANE_MODE. Note: enabling mobile data in airplane mode is not supported on most emulators.
    [Tags]    airplane_mode    conflict
    ${status}=    Get Readable Network Status
    Log    Status returned: ${status}
    Should Be Equal    ${status}    AIRPLANE_MODE