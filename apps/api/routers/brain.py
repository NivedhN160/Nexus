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
from apps.api.models import Thread, Message
from apps.api.routers.metering import record_event, EventCreate
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
    
    # 1. Get or create Thread
    thread = db.query(Thread).filter(Thread.id == req.session_id).first()
    if not thread:
        thread = Thread(id=req.session_id)
        db.add(thread)
        db.commit()

    # 2. Save User Message
    user_msg = Message(thread_id=req.session_id, role="user", content=req.text)
    db.add(user_msg)
    db.commit()
    
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
            model="llama-3.1-8b-instant",
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
                model="llama-3.1-8b-instant",
                messages=messages
            )
            final_answer = second_response.choices[0].message.content
        else:
            final_answer = response_message.content

        # Save AI Responses to DB
        if response_message.tool_calls:
            # Save the tool calls message
            tc_data = [{"id": tc.id, "function": {"name": tc.function.name, "arguments": tc.function.arguments}, "type": tc.type} for tc in response_message.tool_calls]
            llm_tc_msg = Message(thread_id=req.session_id, role="model", tool_calls=tc_data)
            db.add(llm_tc_msg)
            
            # Save tool results
            for idx, tc in enumerate(response_message.tool_calls):
                tool_msg = Message(
                    thread_id=req.session_id, 
                    role="tool", 
                    tool_call_id=tc.id, 
                    name=tc.function.name, 
                    content=json.dumps(tool_cards[idx].dict())
                )
                db.add(tool_msg)
                
            # Save final answer
            if final_answer:
                final_msg = Message(thread_id=req.session_id, role="model", content=final_answer)
                db.add(final_msg)
        else:
            # Save final answer
            final_msg = Message(thread_id=req.session_id, role="model", content=final_answer or "")
            db.add(final_msg)
            
        db.commit()

        # Metering
        input_t = response.usage.prompt_tokens if hasattr(response, 'usage') and response.usage else 0
        output_t = response.usage.completion_tokens if hasattr(response, 'usage') and response.usage else 0
        
        if response_message.tool_calls and 'second_response' in locals():
            input_t += second_response.usage.prompt_tokens if hasattr(second_response, 'usage') and second_response.usage else 0
            output_t += second_response.usage.completion_tokens if hasattr(second_response, 'usage') and second_response.usage else 0
            
        record_event(EventCreate(
            idempotency_key=f"llm_{req.session_id}_{int(time.time()*1000)}",
            event_type="llm",
            input_tokens=input_t,
            output_tokens=output_t
        ), db)

        return BrainResponse(
            answer=final_answer or "",
            tool_cards=tool_cards,
            usage={
                "input_tokens": input_t,
                "output_tokens": output_t
            }
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
