from fastapi import APIRouter, Depends
from pydantic import BaseModel
from packages.shared.auth import get_api_key
from packages.presence.mock_provider import mock_presence

router = APIRouter(dependencies=[Depends(get_api_key)])

class PresenceUpdate(BaseModel):
    is_present: bool

@router.get("/presence")
def get_presence():
    return {"status": "success", "context": mock_presence.get_context(), "is_present": mock_presence.is_present}

@router.post("/presence")
def update_presence(req: PresenceUpdate):
    mock_presence.set_presence(req.is_present)
    return {"status": "success"}
