from enum import Enum
from pydantic import BaseModel
from typing import Dict, Any, Optional

class VerdictLevel(str, Enum):
    SAFE = "SAFE"
    SUSPICIOUS = "SUSPICIOUS"
    NEEDS_APPROVAL = "NEEDS_APPROVAL"
    DENY = "DENY"

class Evidence(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    actor: str = "agent"

class Verdict(BaseModel):
    level: VerdictLevel
    score: int
    reason: str
    tool_name: str
