from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Any, List
from packages.shared.auth import get_api_key
from sqlalchemy.orm import Session
from apps.api.database import get_db
from apps.api.actions.registry import call_tool
import json

router = APIRouter(dependencies=[Depends(get_api_key)])

@router.get("/tools")
def list_tools():
    """
    Expose MCP compatible tool listing.
    """
    return {
        "tools": [
            {
                "name": "leads.get_recent",
                "description": "Fetch the most recent lead submissions from the portfolio widget",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "audit.get_health",
                "description": "Fetch system health and telemetry logs",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "memory.search",
                "description": "Search the local Nexus memory bank",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search term"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "metering.get_usage",
                "description": "Get current API usage limits and stats",
                "inputSchema": {"type": "object", "properties": {}}
            }
        ]
    }

class MCPCallRequest(BaseModel):
    name: str
    arguments: Dict[str, Any]

@router.post("/tools/call")
def call_mcp_tool(req: MCPCallRequest, db: Session = Depends(get_db)):
    """
    Execute an MCP tool respecting Nexus policy and auth.
    """
    try:
        # call_tool returns a pydantic model, we convert to dict
        result = call_tool(req.name, req.arguments, db)
        return {"status": "success", "result": result.dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
