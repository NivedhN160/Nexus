from pydantic import BaseModel
from typing import Any, Optional

class APIErrorResponse(BaseModel):
    error: str
    message: str
    code: str
    details: Optional[Any] = None

class APIResponse(BaseModel):
    status: str = "success"
    data: Optional[Any] = None
