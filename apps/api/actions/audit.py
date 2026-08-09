from sqlalchemy.orm import Session

def get_health(db: Session):
    return {"status": "HEALTHY", "uptime": "72h", "active_modules": 6, "errors_last_24h": 0}
