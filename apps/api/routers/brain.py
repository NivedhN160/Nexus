import os
import json
import time
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from packages.shared.auth import get_api_key
from packages.shared.schemas import ToolResultSchema

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

# Basic Tool implementations
def call_tool(name: str, args: Dict[str, Any]) -> ToolResultSchema:
    start_time = time.time()
    result = None
    error = None
    ok = True
    
    try:
        # Stub tool executions based on spec
        if name == "web_agent.fetch":
            result = {"title": "Example Page", "content": f"Fetched content for {args.get('url')}"}
        elif name == "web_signals.scan":
            result = {"signals": [{"company": c, "score": 8} for c in args.get("companies", [])]}
        elif name == "climate.open":
            result = {"url": "http://localhost:3000/terra-x", "status": "launched"}
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        ok = False
        error = {"code": "TOOL_ERROR", "message": str(e)}
        
    latency_ms = int((time.time() - start_time) * 1000)
    
    return ToolResultSchema(ok=ok, result=result, error=error, latency_ms=latency_ms)


@router.post("/chat", response_model=BrainResponse)
def handle_message(req: BrainRequest):
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        # Fallback to stub behavior if Groq is not configured
        return BrainResponse(
            answer=f"Echo (No LLM key): {req.text}",
            tool_cards=[],
            usage={"input_tokens": 10, "output_tokens": 10}
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
                "name": "web_agent.fetch",
                "description": "Fetch content from a URL",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "The URL to fetch"}
                    },
                    "required": ["url"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "web_signals.scan",
                "description": "Scan companies for buying signals",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "companies": {
                            "type": "array", 
                            "items": {"type": "string"},
                            "description": "List of companies to scan"
                        }
                    },
                    "required": ["companies"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "climate.open",
                "description": "Open the Terra-X climate lab for scenarios",
                "parameters": {
                    "type": "object",
                    "properties": {},
                }
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
                
                tool_res = call_tool(function_name, function_args)
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
