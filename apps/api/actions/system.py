from packages.policy.engine import decide
from packages.policy.types import Evidence, VerdictLevel
from apps.api.models import PendingApproval, DecisionLog
from sqlalchemy.orm import Session
import uuid
import json
import subprocess
from packages.sandbox.runner import run_python_code

def execute_shell(args: dict, db: Session):
    evidence = Evidence(tool_name="system.execute_shell", arguments=args)
    verdict = decide(evidence)
    
    # Log the decision to Postgres
    log = DecisionLog(
        tool_name=evidence.tool_name,
        arguments=args,
        level=verdict.level.value,
        score=verdict.score,
        reason=verdict.reason
    )
    db.add(log)
    
    if verdict.level == VerdictLevel.NEEDS_APPROVAL:
        pending_id = str(uuid.uuid4())
        pending = PendingApproval(
            id=pending_id,
            tool_name=evidence.tool_name,
            arguments=args,
            reason=verdict.reason,
            status="pending"
        )
        db.add(pending)
        db.commit()
        return {"status": "NEEDS_APPROVAL", "message": f"{verdict.reason} Request ID: {pending_id}"}
        
    db.commit()
    
    # Execute the shell safely with timeout
    try:
        cmd = args.get("command", "")
        if not cmd:
            return {"status": "ERROR", "message": "No command provided"}
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return {"status": "EXECUTED", "stdout": process.stdout, "stderr": process.stderr, "returncode": process.returncode}
    except subprocess.TimeoutExpired as e:
        return {"status": "TIMEOUT", "stdout": e.stdout.decode() if e.stdout else ""}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def run_code(args: dict, db: Session):
    evidence = Evidence(tool_name="sandbox.run_code", arguments=args)
    verdict = decide(evidence)
    
    log = DecisionLog(
        tool_name=evidence.tool_name,
        arguments=args,
        level=verdict.level.value,
        score=verdict.score,
        reason=verdict.reason
    )
    db.add(log)
    
    if verdict.level == VerdictLevel.NEEDS_APPROVAL:
        pending_id = str(uuid.uuid4())
        pending = PendingApproval(
            id=pending_id,
            tool_name=evidence.tool_name,
            arguments=args,
            reason=verdict.reason,
            status="pending"
        )
        db.add(pending)
        db.commit()
        return {"status": "NEEDS_APPROVAL", "message": f"{verdict.reason} Request ID: {pending_id}"}
        
    db.commit()
    
    # Execute sandbox
    code = args.get("code", "")
    if not code:
         return {"status": "ERROR", "message": "No code provided"}
    result = run_python_code(code)
    return {"status": "EXECUTED", "output": result}
