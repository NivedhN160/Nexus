from sqlalchemy.orm import Session
from apps.api.models import Submission

def get_recent_leads(db: Session):
    subs = db.query(Submission).order_by(Submission.created_at.desc()).limit(5).all()
    return {"leads": [{"id": s.id, "name": s.name, "email": s.email, "message": s.message, "status": s.status} for s in subs]}
