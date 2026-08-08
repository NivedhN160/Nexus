import os
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import List
from apps.api.database import get_db
from apps.api.models import Campaign, CampaignPost, Post
from packages.shared.auth import get_api_key
from packages.shared.crypto import verify_webhook_signature

# Create a dependency that doesn't check API key for webhooks
router = APIRouter()
protected_router = APIRouter(dependencies=[Depends(get_api_key)])

class ScheduleRequest(BaseModel):
    run_at: datetime

class CampaignCreateResponse(BaseModel):
    campaign_id: int
    post_id: int
    status: str
    
class CampaignPostResponse(BaseModel):
    platform: str
    caption: str
    status: str

class CampaignResponse(BaseModel):
    id: int
    run_at: datetime | None
    status: str
    posts: List[CampaignPostResponse]

    class Config:
        from_attributes = True

@protected_router.post("", response_model=CampaignCreateResponse)
def create_campaign(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    # Check if campaign already exists for this post
    existing = db.query(Campaign).filter(Campaign.post_id == post_id).first()
    if existing:
        return CampaignCreateResponse(campaign_id=existing.id, post_id=post.id, status=existing.status)
        
    campaign = Campaign(post_id=post_id, status="draft")
    db.add(campaign)
    db.flush() # get campaign ID
    
    # Create variants
    ig_post = CampaignPost(
        campaign_id=campaign.id, 
        platform="IG", 
        caption=f"{post.title}\n\n#nexus #ai"
    )
    x_post = CampaignPost(
        campaign_id=campaign.id, 
        platform="X", 
        caption=f"{post.title} {post.url if post.url else ''} #nexus"
    )
    db.add_all([ig_post, x_post])
    db.commit()
    db.refresh(campaign)
    
    return CampaignCreateResponse(campaign_id=campaign.id, post_id=post.id, status=campaign.status)

@protected_router.post("/{campaign_id}/schedule")
def schedule_campaign(campaign_id: int, req: ScheduleRequest, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    campaign.run_at = req.run_at
    campaign.status = "queued"
    
    # In a real system we would push to a Redis queue here (e.g., RQ or Celery)
    # For now we just update the DB status. The worker will poll or listen.
    
    db.commit()
    return {"id": campaign.id, "run_at": campaign.run_at, "status": campaign.status}

@protected_router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    posts = []
    for p in campaign.campaign_posts:
        posts.append(CampaignPostResponse(platform=p.platform, caption=p.caption, status=p.status))
        
    return CampaignResponse(
        id=campaign.id,
        run_at=campaign.run_at,
        status=campaign.status,
        posts=posts
    )

@protected_router.get("", response_model=List[CampaignResponse])
def get_campaigns(db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).order_by(Campaign.id.desc()).all()
    result = []
    for c in campaigns:
        posts = [CampaignPostResponse(platform=p.platform, caption=p.caption, status=p.status) for p in c.campaign_posts]
        result.append(CampaignResponse(id=c.id, run_at=c.run_at, status=c.status, posts=posts))
    return result

@router.post("/webhooks/social-delivery")
async def social_webhook(request: Request, db: Session = Depends(get_db)):
    # Verify HMAC signature
    signature = request.headers.get("X-Signature", "")
    secret = os.getenv("WEBHOOK_SECRET", "default_secret")
    payload = await request.body()
    
    if not verify_webhook_signature(payload, signature, secret):
        raise HTTPException(status_code=401, detail="Invalid signature")
        
    # Process webhook (e.g. delivery success)
    data = await request.json()
    external_id = data.get("external_id")
    status = data.get("status")
    
    if external_id and status:
        cpost = db.query(CampaignPost).filter(CampaignPost.external_id == external_id).first()
        if cpost:
            cpost.status = status
            db.commit()
            
    return {"received": True}

router.include_router(protected_router)
