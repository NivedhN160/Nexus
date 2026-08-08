from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List, Dict, Any
from apps.api.database import get_db
from apps.api.models import Widget, Submission
from packages.shared.auth import get_api_key

public_router = APIRouter()
admin_router = APIRouter(dependencies=[Depends(get_api_key)])

class WidgetCreate(BaseModel):
    name: str
    config_json: Dict[str, Any]

class SubmissionCreate(BaseModel):
    name: str
    email: str
    message: str
    honeypot: str = "" # Anti-spam field

class SubmissionResponse(BaseModel):
    id: int
    name: str
    email: str
    message: str
    geo: str | None
    status: str

    class Config:
        from_attributes = True

# --- ADMIN ROUTES ---

@admin_router.post("/widgets")
def create_widget(widget: WidgetCreate, db: Session = Depends(get_db)):
    db_widget = Widget(name=widget.name, config_json=widget.config_json)
    db.add(db_widget)
    db.commit()
    db.refresh(db_widget)
    return {"id": db_widget.id, "name": db_widget.name}

@admin_router.get("/widgets/{widget_id}")
def get_widget(widget_id: int, db: Session = Depends(get_db)):
    widget = db.query(Widget).filter(Widget.id == widget_id).first()
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")
    return {"id": widget.id, "name": widget.name, "config_json": widget.config_json}

@admin_router.get("/submissions", response_model=List[SubmissionResponse])
def get_submissions(db: Session = Depends(get_db)):
    return db.query(Submission).order_by(Submission.created_at.desc()).all()

@admin_router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    count = db.query(func.count(Submission.id)).scalar()
    # Mocking honeypot blocked count for now
    return {"submissions_total": count, "honeypot_blocked": 0}


# --- PUBLIC ROUTES ---

@public_router.get("/widgets/{widget_id}/config")
def get_widget_config(widget_id: int, db: Session = Depends(get_db)):
    # CORS enabled public endpoint
    widget = db.query(Widget).filter(Widget.id == widget_id).first()
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")
    return widget.config_json

@public_router.post("/widgets/{widget_id}/submissions")
async def submit_lead(widget_id: int, req: Request, sub: SubmissionCreate, db: Session = Depends(get_db)):
    # 1. Validate payload size
    if len(sub.message) > 5000:
        raise HTTPException(status_code=400, detail="Message too long")
        
    # 2. Rate limit (Stub) - would normally check Redis by IP
    client_ip = req.client.host if req.client else "unknown"
    
    # 3. Honeypot check
    if sub.honeypot != "":
        # Silently drop
        return {"status": "success", "message": "Thank you for your submission."}
        
    # 4. Geo fallback
    geo = "US" # Stub for geo lookup
    
    # 5. Store
    db_sub = Submission(
        widget_id=widget_id,
        name=sub.name,
        email=sub.email,
        message=sub.message,
        geo=geo,
        status="new"
    )
    db.add(db_sub)
    db.commit()
    
    return {"status": "success", "message": "Thank you for your submission."}

@public_router.get("/widget.js")
def get_widget_js():
    # Serve the script
    js_content = """
    console.log('Nexus Lead Widget Loaded');
    // Implement widget injection logic here
    """
    return Response(content=js_content, media_type="application/javascript")

router = APIRouter()
router.include_router(public_router)
router.include_router(admin_router, prefix="/admin")
