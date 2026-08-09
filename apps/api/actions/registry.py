import time
from typing import Dict, Any
from sqlalchemy.orm import Session
from packages.shared.schemas import ToolResultSchema

# Action Handlers
from .leads import get_recent_leads
from .audit import get_health
from .system import execute_shell, run_code
from .memory import search_memory
from .climate import open_climate

def call_tool(name: str, args: Dict[str, Any], db: Session) -> ToolResultSchema:
    start_time = time.time()
    result = None
    error = None
    ok = True
    
    try:
        if name == "leads.get_recent":
            result = get_recent_leads(db)
        elif name == "audit.get_health":
            result = get_health(db)
        elif name == "system.execute_shell":
            result = execute_shell(args)
            if "NEEDS_APPROVAL" in str(result):
                ok = False
                error = {"code": "NEEDS_APPROVAL", "message": result.get("message")}
                result = None
        elif name == "sandbox.run_code":
            result = run_code(args)
            if "NEEDS_APPROVAL" in str(result):
                ok = False
                error = {"code": "NEEDS_APPROVAL", "message": result.get("message")}
                result = None
        elif name == "memory.search":
            result = search_memory(args)
            if "state" in result and result["state"] == "LOW_CONFIDENCE":
                ok = False
                error = {"code": "LOW_CONFIDENCE", "message": "No direct matches found. Please ask clarifying questions or rewrite query."}
                result = None
        elif name == "climate.open":
            result = open_climate()
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        ok = False
        error = {"code": "TOOL_ERROR", "message": str(e)}
        
    latency_ms = int((time.time() - start_time) * 1000)
    
    return ToolResultSchema(ok=ok, result=result, error=error, latency_ms=latency_ms)
