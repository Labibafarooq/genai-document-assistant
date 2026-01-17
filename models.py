from dataclasses import dataclass
from typing import List, Optional, Literal


@dataclass
class DataPoint:
    text: str
    source: Optional[str] = None


@dataclass
class AnalystOutput:
    topic: str
    data_points: List[DataPoint]


@dataclass
class DraftInput:
    topic: str
    data_points: List[DataPoint]
    edit_request: Optional[str]
    version: int
    grounded: bool  # NEW: whether we found dataset evidence


@dataclass
class DraftOutput:
    subject: str
    body: str
    version: int


ApprovalDecision = Literal["approve", "edit_request"]


@dataclass
class ApprovalOutput:
    decision: ApprovalDecision
    edit_request: Optional[str] = None
