import os
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List, Dict, Any
from apps.api.database import get_db
from apps.api.models import MeteringEvent
from packages.shared.auth import get_api_key
from packages.shared.pricing import PricingHelpers
import json

router = APIRouter()
protected_router = APIRouter(dependencies=[Depends(get_api_key)])

# Hardcoded quota for v1 (in micro-cents) e.g., $10.00 = 1,000,000,000 microcents
MONTHLY_QUOTA = 1_000_000_000 

class EventCreate(BaseModel):
    idempotency_key: str
    event_type: str
    input_tokens: int = 0
    output_tokens: int = 0
    # Add other params like image count if needed
    
class EventResponse(BaseModel):
    id: int
    idempotency_key: str
    event_type: str
    cost_microcents: int

@protected_router.post("/events", response_model=EventResponse)
def record_event(event: EventCreate, db: Session = Depends(get_db)):
    # 1. Idempotency check
    existing = db.query(MeteringEvent).filter(MeteringEvent.idempotency_key == event.idempotency_key).first()
    if existing:
        return EventResponse(
            id=existing.id,
            idempotency_key=existing.idempotency_key,
            event_type=existing.event_type,
            cost_microcents=existing.cost_microcents
        )
        
    # 2. Calculate cost
    cost = 0
    if event.event_type == "llm":
        # e.g., $0.50 per 1M input, $1.50 per 1M output (Llama 3 70B roughly)
        cost = PricingHelpers.calculate_token_cost(event.input_tokens, event.output_tokens, 0.50, 1.50)
    elif event.event_type == "vision":
        # e.g., $0.01 per image -> 1,000,000 microcents
        cost = 1_000_000
        
    # 3. Quota check
    total_spend = db.query(func.sum(MeteringEvent.cost_microcents)).scalar() or 0
    if total_spend + cost > MONTHLY_QUOTA:
        raise HTTPException(status_code=402, detail="Payment Required: Quota exceeded")
        
    # 4. Record
    db_event = MeteringEvent(
        idempotency_key=event.idempotency_key,
        event_type=event.event_type,
        cost_microcents=cost
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return EventResponse(
        id=db_event.id,
        idempotency_key=db_event.idempotency_key,
        event_type=db_event.event_type,
        cost_microcents=db_event.cost_microcents
    )

@protected_router.get("/usage")
def get_usage(db: Session = Depends(get_db)):
    total_spend = db.query(func.sum(MeteringEvent.cost_microcents)).scalar() or 0
    events_count = db.query(func.count(MeteringEvent.id)).scalar() or 0
    
    return {
        "total_spend_microcents": total_spend,
        "total_spend_usd": PricingHelpers.microcents_to_usd(total_spend),
        "quota_microcents": MONTHLY_QUOTA,
        "quota_usd": PricingHelpers.microcents_to_usd(MONTHLY_QUOTA),
        "events_count": events_count,
        "percentage_used": min(100.0, (total_spend / MONTHLY_QUOTA) * 100) if MONTHLY_QUOTA > 0 else 100.0
    }

router.include_router(protected_router)
