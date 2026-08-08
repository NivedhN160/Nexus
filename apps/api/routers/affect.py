from fastapi import APIRouter, Depends
from packages.shared.auth import get_api_key
import random
import time

router = APIRouter(dependencies=[Depends(get_api_key)])

@router.get("/status")
def get_affect_status():
    # Stub emotion/frustration status
    # In a real system, a background CV pipeline would push updates to Redis
    # and we would fetch the latest state here.
    states = ["calm", "calm", "calm", "tense", "frustrated"]
    state = random.choice(states)
    
    score = 0.1 if state == "calm" else (0.6 if state == "tense" else 0.9)
    
    return {
        "state": state,
        "score": score,
        "ts": int(time.time())
    }
