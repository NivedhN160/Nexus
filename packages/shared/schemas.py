from pydantic import BaseModel
from typing import Optional, Any, Dict

class ErrorSchema(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class ToolResultSchema(BaseModel):
    ok: bool
    result: Optional[Any] = None
    error: Optional[ErrorSchema] = None
    latency_ms: int
