*** Settings ***
Library    AppiumLibrary
Library    NetworkStatus.py

*** Variables ***
${REMOTE_URL}           http://localhost:4723
${PLATFORM_NAME}        Android
${DEVICE_NAME}          Emulator
${UDID}                 emulator-5554

*** Keywords ***
Initialize Appium Connection
    Open Application    ${REMOTE_URL}
    ...                 automationName=uiautomator2
    ...                 platformName=${PLATFORM_NAME}
    ...                 deviceName=${DEVICE_NAME}
    ...                 udid=${UDID}
    ...                 noReset=true
    ...                 skipServerInstallation=true
    ...                 skipDeviceInitialization=true
    ...                 newCommandTimeout=300
    