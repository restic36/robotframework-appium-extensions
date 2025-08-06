*** Settings ***
Library    AppiumLibrary
Library    OperatingSystem
Library    Collections
Library    BuiltIn
Library    VisibleElements.py

*** Variables ***
${REMOTE_URL}           http://localhost:4723
${PLATFORM_NAME}        Android
${DEVICE_NAME}          Emulator
${UDID}                 emulator-5554
${APP_PACKAGE}          org.wikipedia
${APP_ACTIVITY}         org.wikipedia.main.MainActivity

*** Keywords ***
Open Wikipedia App
    Open Application    ${REMOTE_URL}
    ...                 automationName=uiautomator2
    ...                 platformName=${PLATFORM_NAME}
    ...                 deviceName=${DEVICE_NAME}
    ...                 udid=${UDID}
    ...                 autoGrantPermissions=true
    ...                 appPackage=${APP_PACKAGE}
    ...                 appActivity=${APP_ACTIVITY}
    ...                 newCommandTimeout=300

Close Wikipedia App
    Close Application