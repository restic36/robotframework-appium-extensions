# Network Status — AppiumLibrary Extension

`NetworkStatus` is a custom keyword designed to simplify and standardize network status detection in Android devices during tests using Appium and Robot Framework. It leverages the `driver.network_connection` property to interpret the device's network status and return a readable, meaningful result.

---

## Purpose

- Clearly and reliably interpret network status using Appium’s `bitmasks` values
- Return a human-readable string for the current network type (Wi-Fi, mobile data, airplane mode, or no connection)
- Validate that the device is online before running tests that require connectivity
- Confirm that offline scenarios are properly configured
- Differentiate between Wi-Fi and mobile data connections
- Ensure robust behavior across real devices and emulators

---

## How It Works

The Appium method `driver.network_connection` returns an integer bitmask based on the active connection:

| Value | Network Type             |
|-------|--------------------------|
| 0     | No connection            |
| 1     | Airplane mode            |
| 2     | Wi-Fi only               |
| 4     | Mobile data only         |
| 6     | Wi-Fi + mobile data      |

The keyword also checks airplane mode using ADB (`adb shell settings get global airplane_mode_on`) and gives it priority when active, even if Wi-Fi or data are enabled.
If none of the known cases match, a final fallback returns `UNKNOWN`, which covers unusual bitmask values or unexpected status read failures.
Result mapping:

- [No active connection?] → `NONE`
- [Airplane mode is on?] → `AIRPLANE_MODE`
- [Wi-Fi only?] → `WIFI_ONLY`
- [Mobile data only?] → `DATA_ONLY`
- [Both Wi-Fi and mobile data?] → `WIFI_AND_DATA`
- [Unrecognized or inconsistent status?] → `UNKNOWN`

---

## How To Execute

To execute all test cases:  

```bash
robot NetworkStatus.robot
```

Make sure that:
- `AppiumLibrary` and the `NetworkStatus`keyword are correctly imported
- The emulator or physical device is connected and online

---

## Technical Details

- Built to work with AppiumLibrary and Robot Framework
- Uses Appium's `driver.network_connection`
- Designed for simplicity, reliability, and maintainability

---

## Code Structure

- Implemented as a class (`NetworkStatusitmask`) with `ROBOT_LIBRARY_SCOPE = GLOBAL`
- Modular architecture with helper methods  (`interpretar_bitmask`, `definir_status_rede`, etc.)
- Requires no input arguments and contains no complex validation logic
- Leverages ADB to detect airplane mode for more accurate status

---

## Test Structure

The keyword has been validated through:

### Mocked Tests

- **No connection (NONE) – bitmask: 0**
- **Airplane mode enabled (AIRPLANE_MODE) – bitmask: 1**
- **Wi-Fi only – bitmask: 2**
- **Mobile data only – bitmask: 4**
- **Wi-Fi and mobile data – bitmask: 6**
- **Unknown bitmask (UNKNOWN) – bitmask: 8**

### Emulator Tests

- **Wi-Fi only active**
- **Mobile data only active**
- **Wi-Fi and mobile data active**
- **Airplane mode enabled (Wi-Fi and data disabled)**
- **No network active**
- **Airplane mode with Wi-Fi enabled**

### Physical Device Tests *(Pending)*

_Not yet validated in physical devices. Will be tested and updated soon._