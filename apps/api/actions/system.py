from packages.policy.engine import decide
from packages.policy.types import Evidence, VerdictLevel

def execute_shell(args: dict):
    evidence = Evidence(tool_name="system.execute_shell", arguments=args)
    verdict = decide(evidence)
    
    if verdict.level == VerdictLevel.NEEDS_APPROVAL:
        return {"status": "NEEDS_APPROVAL", "message": verdict.reason}
        
    return {"status": "EXECUTED", "stdout": "Mock execution output"}

def run_code(args: dict):
    evidence = Evidence(tool_name="run_code", arguments=args)
    verdict = decide(evidence)
    
    if verdict.level == VerdictLevel.NEEDS_APPROVAL:
        return {"status": "NEEDS_APPROVAL", "message": verdict.reason}
        
    # Would run sandbox if approved/safe
    return {"status": "EXECUTED", "output": "Sandbox output mock"}
