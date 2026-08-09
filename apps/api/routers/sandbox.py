from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from packages.sandbox.runner import run_python_code
from packages.shared.auth import get_api_key

router = APIRouter(dependencies=[Depends(get_api_key)])

class RunRequest(BaseModel):
    code: str
    timeout: int = 5

@router.post("/run")
def execute_sandbox(req: RunRequest):
    result = run_python_code(req.code, req.timeout)
    return result
