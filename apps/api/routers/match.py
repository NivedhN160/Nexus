from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from apps.api.database import get_db
from apps.api.models import MatchThread, MatchMessage
from packages.shared.auth import get_api_key

router = APIRouter(dependencies=[Depends(get_api_key)])

class SearchRequest(BaseModel):
    query: str

class MatchCandidate(BaseModel):
    id: str
    name: str
    score: float
    tags: List[str]

class ThreadCreateResponse(BaseModel):
    thread_id: int
    status: str

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    sender: str
    content: str

class ThreadResponse(BaseModel):
    id: int
    status: str
    messages: List[MessageResponse]
    
    class Config:
        from_attributes = True

@router.post("/search", response_model=List[MatchCandidate])
def search_match(req: SearchRequest):
    # Stub semantic search
    # In a real system, would embed the query and query a vector store
    return [
        MatchCandidate(id="p1", name="Alice Developer", score=0.92, tags=["backend", "python"]),
        MatchCandidate(id="p2", name="Bob Designer", score=0.85, tags=["ui", "figma"])
    ]

@router.post("/threads", response_model=ThreadCreateResponse)
def create_thread(db: Session = Depends(get_db)):
    thread = MatchThread(status="active")
    db.add(thread)
    db.commit()
    db.refresh(thread)
    return ThreadCreateResponse(thread_id=thread.id, status=thread.status)

@router.post("/threads/{thread_id}/messages", response_model=MessageResponse)
def send_message(thread_id: int, msg: MessageCreate, db: Session = Depends(get_db)):
    thread = db.query(MatchThread).filter(MatchThread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
        
    db_msg = MatchMessage(thread_id=thread_id, sender="user", content=msg.content)
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    
    return MessageResponse(
        id=db_msg.id,
        sender=db_msg.sender,
        content=db_msg.content
    )

@router.post("/threads/{thread_id}/confirm")
def confirm_thread(thread_id: int, db: Session = Depends(get_db)):
    thread = db.query(MatchThread).filter(MatchThread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
        
    thread.status = "confirmed"
    db.commit()
    return {"id": thread.id, "status": thread.status}

@router.get("/threads/{thread_id}", response_model=ThreadResponse)
def get_thread(thread_id: int, db: Session = Depends(get_db)):
    thread = db.query(MatchThread).filter(MatchThread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
        
    messages = [MessageResponse(id=m.id, sender=m.sender, content=m.content) for m in thread.messages]
    return ThreadResponse(id=thread.id, status=thread.status, messages=messages)
