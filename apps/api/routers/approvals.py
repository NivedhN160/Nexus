import json
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import DecisionLog, PendingApproval
from packages.shared.auth import get_api_key

router = APIRouter(dependencies=[Depends(get_api_key)])

@router.get("/decisions")
def get_decisions(db: Session = Depends(get_db)):
    logs = db.query(DecisionLog).order_by(DecisionLog.created_at.desc()).limit(50).all()
    return {"decisions": [{"id": l.id, "tool_name": l.tool_name, "level": l.level, "score": l.score, "reason": l.reason, "created_at": l.created_at} for l in logs]}

@router.get("/pending")
def get_pending_approvals(db: Session = Depends(get_db)):
    pending = db.query(PendingApproval).filter_by(status="pending").order_by(PendingApproval.created_at.desc()).all()
    return {"pending": [{"id": p.id, "tool_name": p.tool_name, "reason": p.reason, "status": p.status, "created_at": p.created_at} for p in pending]}

@router.post("/{decision_id}/approve")
def approve_decision(decision_id: str, db: Session = Depends(get_db)):
    pending = db.query(PendingApproval).filter_by(id=decision_id).first()
    if not pending:
        raise HTTPException(status_code=404, detail="Pending approval not found")
    
    if pending.status != "pending":
        raise HTTPException(status_code=400, detail="Approval is not pending")
        
    pending.status = "approved"
    db.commit()
    return {"status": "approved"}

@router.post("/{decision_id}/deny")
def deny_decision(decision_id: str, db: Session = Depends(get_db)):
    pending = db.query(PendingApproval).filter_by(id=decision_id).first()
    if not pending:
        raise HTTPException(status_code=404, detail="Pending approval not found")
        
    if pending.status != "pending":
        raise HTTPException(status_code=400, detail="Approval is not pending")
        
    pending.status = "denied"
    db.commit()
    return {"status": "denied"}
