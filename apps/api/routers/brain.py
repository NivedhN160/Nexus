import os
import json
import time
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from packages.shared.auth import get_api_key
from packages.shared.schemas import ToolResultSchema
from sqlalchemy.orm import Session
from apps.api.database import get_db
from apps.api.actions.registry import call_tool

from groq import Groq

router = APIRouter(dependencies=[Depends(get_api_key)])

class BrainRequest(BaseModel):
    text: str
    session_id: str
    history: List[Dict[str, str]] = []

class BrainResponse(BaseModel):
    answer: str
    tool_cards: List[ToolResultSchema]
    usage: Dict[str, int]



@router.post("/chat", response_model=BrainResponse)
def handle_message(req: BrainRequest, db: Session = Depends(get_db)):
    # Free-by-default architecture: Local models first
    llm_provider = os.getenv("LLM_PROVIDER", "local")
    cloud_enabled = os.getenv("NEXUS_CLOUD_LLM", "0") == "1"
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    # If cloud is disabled or key is missing, use local stub / NGPT logic
    if not cloud_enabled or not groq_api_key:
        return BrainResponse(
            answer=f"[Local AI / ZigNGPT]: Received your message -> '{req.text}'. (Running completely local. No cloud API used.)",
            tool_cards=[],
            usage={"input_tokens": 10, "output_tokens": 15}
        )
        
    client = Groq(api_key=groq_api_key)
    
    messages = [
        {"role": "system", "content": "You are Nexus, a personal AI operations platform agent. You manage content, leads, social scheduling, and research."}
    ]
    messages.extend(req.history)
    messages.append({"role": "user", "content": req.text})
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "leads.get_recent",
                "description": "Fetch the most recent lead submissions from the portfolio widget",
                "parameters": {"type": "object", "properties": {}}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "audit.get_health",
                "description": "Fetch system health and telemetry logs",
                "parameters": {"type": "object", "properties": {}}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "system.execute_shell",
                "description": "DANGEROUS: Execute a shell command on the host machine",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Command to run"}
                    },
                    "required": ["command"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "sandbox.run_code",
                "description": "Run untrusted Python code in the sandbox",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Python code to execute"}
                    },
                    "required": ["code"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "memory.search",
                "description": "Search the local Nexus memory bank",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search term"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "climate.open",
                "description": "Open the Terra-X climate lab for scenarios",
                "parameters": {"type": "object", "properties": {}}
            }
        }
    ]
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_cards = []
        
        # Handle tool calls
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                tool_res = call_tool(function_name, function_args, db)
                tool_cards.append(tool_res)
                
                messages.append(response_message)
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(tool_res.dict())
                })
            
            # Second call to LLM after tool results
            second_response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=messages
            )
            final_answer = second_response.choices[0].message.content
        else:
            final_answer = response_message.content

        return BrainResponse(
            answer=final_answer or "",
            tool_cards=tool_cards,
            usage={
                "input_tokens": response.usage.prompt_tokens if hasattr(response, 'usage') and response.usage else 0,
                "output_tokens": response.usage.completion_tokens if hasattr(response, 'usage') and response.usage else 0
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
