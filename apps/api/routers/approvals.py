import json
import os
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from packages.shared.auth import get_api_key

router = APIRouter(dependencies=[Depends(get_api_key)])
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "decisions.jsonl")

@router.get("/decisions")
def get_decisions():
    if not os.path.exists(LOG_FILE):
        return {"decisions": []}
    
    decisions = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            if line.strip():
                decisions.append(json.loads(line))
    
    # Return last 50 decisions, newest first
    return {"decisions": decisions[::-1][:50]}
