import re
from typing import Dict, Any, Tuple

# Simple denylist
BLOCKED_KEYWORDS = ["drop table", "rm -rf", "delete from"]

def check_input(prompt: str) -> Tuple[bool, str]:
    """Check user input for dangerous keywords"""
    lower_prompt = prompt.lower()
    for kw in BLOCKED_KEYWORDS:
        if kw in lower_prompt:
            return False, f"Input blocked due to restricted keyword: {kw}"
    return True, "ok"

def check_output(response: str) -> Tuple[bool, str]:
    """Check AI output for PII or dangerous patterns"""
    # Just a placeholder for output redaction/blocking
    return True, "ok"

def check_tool_call(tool_name: str, args: Dict[str, Any]) -> Tuple[bool, str]:
    """Ensure tool execution is safe"""
    if tool_name == "system.execute_shell":
        # Additional checks for shell commands
        cmd = args.get("command", "").lower()
        for kw in BLOCKED_KEYWORDS:
            if kw in cmd:
                return False, f"Dangerous command blocked: {kw}"
    return True, "ok"
