from .types import Evidence, VerdictLevel

# Hardcoded rules for deterministic evaluation (StadiumMind pattern)
DANGEROUS_TOOLS = {
    "system.execute_shell": 100,
    "file.delete": 100,
    "run_code": 80,
}

SUSPICIOUS_ARGS = [
    "rm -rf", "mkfs", "> /dev/sda", "DROP TABLE"
]

def score_evidence(evidence: Evidence) -> int:
    score = 0
    
    # Base score by tool
    if evidence.tool_name in DANGEROUS_TOOLS:
        score += DANGEROUS_TOOLS[evidence.tool_name]
        
    # Arg scanning
    for k, v in evidence.arguments.items():
        if isinstance(v, str):
            for sus in SUSPICIOUS_ARGS:
                if sus in v:
                    score += 50
                    
    return score

def map_score_to_level(score: int) -> VerdictLevel:
    if score >= 100:
        return VerdictLevel.NEEDS_APPROVAL
    if score >= 50:
        return VerdictLevel.SUSPICIOUS
    return VerdictLevel.SAFE
