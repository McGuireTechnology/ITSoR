from typing import NewType

FrameworkId = NewType("FrameworkId", str)
DomainId = NewType("DomainId", str)
ControlId = NewType("ControlId", str)
ControlLinkId = NewType("ControlLinkId", str)
ControlExampleId = NewType("ControlExampleId", str)
ControlGuidanceId = NewType("ControlGuidanceId", str)

__all__ = [
    "FrameworkId",
    "DomainId",
    "ControlId",
    "ControlLinkId",
    "ControlExampleId",
    "ControlGuidanceId",
]