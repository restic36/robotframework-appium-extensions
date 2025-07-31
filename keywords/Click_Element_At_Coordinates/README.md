# Touch at Offset on Element

Implementation of a Robot Framework keyword to perform a touch action at a specific offset (absolute or relative) on a web/app element using W3C Actions

# Installation 

1-Place the AppiumClick class file (e.g., AppiumClick.py) in a Python package accessible by your Robot project.

2-Ensure Robot Framework and AppiumLibrary are installed

# Keyword:ClickC

Performs a tap on the element found by locator, at the point specified by xoffset and yoffset.

# Parameters

locator – locator of the target element (required)

xoffset – X offset: can be in pixels (e.g., 100) or relative percentage (e.g., 0.5 for 50% of element width) (required)

yoffset – Y offset: same behavior as xoffset but relative to height (required)

# Notes:

* Offsets >= 0 and <= 1 are treated as percentage; other values are pixels.

* Ensures click does not occur outside visible screen area.

* Requires AppiumLibrary instance available in Robot context.

* Raises descriptive exceptions if driver is absent, element not found, offsets invalid, or click fails.