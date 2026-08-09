from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from apps.api.database import get_db
from apps.api.models import MatchThread, MatchMessage, MatchProfile
from packages.shared.auth import get_api_key
import uuid

router = APIRouter(dependencies=[Depends(get_api_key)])

class SearchRequest(BaseModel):
    query: str

class ProfileCreate(BaseModel):
    name: str
    tags: List[str]
    bio: str

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

@router.post("/profiles")
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    db_profile = MatchProfile(
        id=str(uuid.uuid4()),
        name=profile.name,
        tags=profile.tags,
        bio=profile.bio,
        embedding=[0.1, 0.2, 0.3] # Stub embedding
    )
    db.add(db_profile)
    db.commit()
    return {"id": db_profile.id, "status": "created"}

@router.post("/search", response_model=List[MatchCandidate])
def search_match(req: SearchRequest, db: Session = Depends(get_db)):
    # Local semantic search simulation over MatchProfiles
    profiles = db.query(MatchProfile).all()
    results = []
    
    query_lower = req.query.lower()
    for p in profiles:
        score = 0.5
        for tag in p.tags:
            if tag.lower() in query_lower:
                score += 0.2
        if p.bio and query_lower in p.bio.lower():
            score += 0.3
            
        score = min(0.99, score)
        if score >= 0.5:
            results.append(MatchCandidate(id=p.id, name=p.name, score=score, tags=p.tags))
            
    results.sort(key=lambda x: x.score, reverse=True)
    return results

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
