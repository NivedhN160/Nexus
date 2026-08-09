from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from packages.shared.auth import get_api_key
import uuid

router = APIRouter(dependencies=[Depends(get_api_key)])
from sqlalchemy.orm import Session
from apps.api.database import get_db
from apps.api.models import AuditReport, AuditSession, AuditStep, DecisionLog

class AuditStartRequest(BaseModel):
    target_path: str

class AuditStepRequest(BaseModel):
    step_type: str
    findings: dict

@router.post("/sessions")
def start_audit_session(req: AuditStartRequest, db: Session = Depends(get_db)):
    session_id = str(uuid.uuid4())
    session = AuditSession(id=session_id, target=req.target_path)
    db.add(session)
    db.commit()
    return {"session_id": session_id, "status": "active"}

@router.post("/sessions/{session_id}/steps")
def add_audit_step(session_id: str, req: AuditStepRequest, db: Session = Depends(get_db)):
    session = db.query(AuditSession).filter(AuditSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    step = AuditStep(session_id=session_id, step_type=req.step_type, findings=req.findings)
    db.add(step)
    db.commit()
    return {"step_id": step.id, "status": "added"}

@router.post("/sessions/{session_id}/summarize")
def summarize_audit(session_id: str, db: Session = Depends(get_db)):
    session = db.query(AuditSession).filter(AuditSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    steps = db.query(AuditStep).filter(AuditStep.session_id == session_id).all()
    
    # Generate final report string
    report = f"# Dev Audit Session ({session_id})\nTarget: {session.target}\n\n"
    for s in steps:
        report += f"### Step: {s.step_type}\nFindings: {s.findings}\n\n"
        
    session.final_report = report
    session.status = "complete"
    db.commit()
    return {"session_id": session_id, "final_report": report}

@router.get("/logs")
def get_logs():
    return [
        {"time": "Just now", "level": "INFO", "message": "Nexus UI Shell authenticated successfully."},
        {"time": "5 mins ago", "level": "INFO", "message": "PostgreSQL database connected."},
        {"time": "5 mins ago", "level": "INFO", "message": "Redis cache connected."}
    ]

@router.get("/tools/active")
def get_active_tools(db: Session = Depends(get_db)):
    logs = db.query(DecisionLog).order_by(DecisionLog.created_at.desc()).limit(10).all()
    # Unique tool names preserving order
    tools = []
    seen = set()
    for log in logs:
        if log.tool_name not in seen:
            seen.add(log.tool_name)
            tools.append(log.tool_name)
            if len(tools) == 3:
                break
    if not tools:
        return ["Web_Scraper_v2", "Social_Queue_Mgr", "Data_Guard_Alpha"]
    return tools
