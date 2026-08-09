import pytest
from packages.policy.types import Evidence, VerdictLevel
from packages.policy.engine import decide
from packages.policy.rules import score_evidence

def test_safe_tool():
    ev = Evidence(tool_name="leads.get_recent", arguments={})
    score = score_evidence(ev)
    assert score == 0
    verdict = decide(ev)
    assert verdict.level == VerdictLevel.SAFE

def test_dangerous_tool():
    ev = Evidence(tool_name="system.execute_shell", arguments={"command": "echo 1"})
    verdict = decide(ev)
    assert verdict.level == VerdictLevel.NEEDS_APPROVAL

def test_suspicious_args():
    ev = Evidence(tool_name="sandbox.run_code", arguments={"code": "rm -rf /"})
    verdict = decide(ev)
    assert verdict.level == VerdictLevel.NEEDS_APPROVAL
