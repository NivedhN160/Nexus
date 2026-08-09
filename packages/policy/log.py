import json
import os
from datetime import datetime
from .types import Evidence, Verdict

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "decisions.jsonl")

def log_decision(evidence: Evidence, verdict: Verdict):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "evidence": evidence.dict(),
        "verdict": verdict.dict()
    }
    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
