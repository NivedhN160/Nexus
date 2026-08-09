from .types import Evidence, Verdict, VerdictLevel
from .rules import score_evidence, map_score_to_level
from .log import log_decision

def decide(evidence: Evidence) -> Verdict:
    score = score_evidence(evidence)
    level = map_score_to_level(score)
    
    reason = f"Scored {score} based on deterministic rules."
    if level == VerdictLevel.NEEDS_APPROVAL:
        reason = f"Tool {evidence.tool_name} requires explicit human approval."
        
    verdict = Verdict(
        level=level,
        score=score,
        reason=reason,
        tool_name=evidence.tool_name
    )
    
    log_decision(evidence, verdict)
    return verdict
