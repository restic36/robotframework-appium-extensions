Keyword ChangeTheme — AppiumLibrary Extension

ChangeTheme is a custom keyword library for Robot Framework designed to change and validate Android device system themes (Light, Dark, Auto) during automated tests using Appium.
It leverages ADB commands to dynamically switch UI modes, ensuring reliable testing across different scenarios.

🎯 Purpose

Switch between Light and Dark system themes

Reset theme to Auto (system default)

Dynamically set the device UDID for multi-device testing

Provide consistent behavior across devices and emulators

Validate that the theme was correctly applied

Enable UI testing under different visual configurations

Support apps that behave differently under light/dark modes

⚙️ How It Works

The keyword uses ADB shell commands to interact with the system setting ui_night_mode:

Code	Mode	Description
0	Auto	System default, automatic theme handling
1	Light	Light theme
2	Dark	Dark theme

Validation ensures that the applied mode matches the expected theme.

▶️ How To Execute
Basic Usage
Set Device UDID    emulator-5554
Change To Dark Theme
${theme}=    Get Current Theme
Should Be Equal    ${theme}    dark

Test Suite Execution

Run your test suite:

robot test_change_theme.robot


Make sure that:

AppiumLibrary and ChangeTheme are imported

A device or emulator is connected and responsive

ADB is installed and accessible in PATH

📌 Parameters

Set Device UDID
udid (str) – Device unique identifier. Required when multiple devices are connected.

Change To Dark Theme
verify (bool) – Optional. If True, validates that the change was applied (default: True).

Change To Light Theme
Same as above.

Get Current Theme
Returns: "auto", "light", "dark", or "unknown".

Toggle Theme
Switches between dark/light. If in auto mode, defaults to dark.

Reset Theme To Auto
Resets system theme to automatic handling.

📖 Examples

Switch to dark theme:

Change To Dark Theme


Switch to light theme:

Change To Light Theme


Get current theme:

${theme}=    Get Current Theme
Log    Current theme is ${theme}


Toggle theme:

Toggle Theme


Reset theme to auto:

Reset Theme To Auto

🔬 Technical Details

Built on top of AppiumLibrary and Robot Framework

Uses ADB shell settings commands for theme switching

Provides logging and error handling for failures

Supports multiple devices by setting UDID dynamically

Returns True on successful execution

✅ Test Scenarios
Successful Theme Switches

Dark theme applied successfully

Light theme applied successfully

Auto reset works as expected

Toggle alternates between dark/light

Validation Tests

Wrong UDID (invalid device)

Failure to apply theme (ADB error)

Verification mismatch (expected vs actual)

⚠️ Error Handling

The keyword provides clear error messages for:

Missing or invalid UDID

Failure to execute ADB commands

Timeout during command execution

Theme verification mismatch

💡 Use Cases

Test app behavior under Light/Dark themes

Validate UI rendering in different visual modes

Automate theme-sensitive workflows

Ensure consistent UX across themes

Enable cross-device testing with dynamic UDID assignment