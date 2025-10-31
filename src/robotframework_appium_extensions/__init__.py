"""
RobotFramework Appium Extensions
================================
Additional keywords for Robot Framework's AppiumLibrary.

Developed within the Technology Residency Program, executed by CEPEDI,
coordinated by SOFTEX, and supported by MCTI, with the participation
of Positivo Tecnologia as the partner company that proposed the development challenge.

This package can be imported in two ways:
- Full import:     `Library    robotframework_appium_extensions`
  → Loads all keywords automatically.

- Specific import: `Library    robotframework_appium_extensions.keywords.ClickElements`
  → Loads only the desired keyword module.
"""

from .keywords.ChangeTheme import *
from .keywords.ClickElements import *
from .keywords.CompareScreenshots import *
from .keywords.NetworkStatus import *
from .keywords.PerformLongPress import *
from .keywords.PerformPinch import *
from .keywords.PerformZoom import *
from .keywords.ScrollInside import *
from .keywords.ScrollToElement import *
from .keywords.SwipeElement import *
from .keywords.TapAtPercentage import *
from .keywords.TapElementAtCoordinates import *
from .keywords.TerminateApplicationExtension import *
from .keywords.VisibleElements import *
from .keywords.WaitMultipleElements import *

__all__ = [
    "ChangeTheme",
    "ClickElements",
    "CompareScreenshots",
    "NetworkStatus",
    "PerformLongPress",
    "PerformPinch",
    "PerformZoom",
    "ScrollInside",
    "ScrollToElement",
    "SwipeElement",
    "TapAtPercentage",
    "TapElementAtCoordinates",
    "TerminateApplicationExtension",
    "VisibleElements",
    "WaitMultipleElements",
]