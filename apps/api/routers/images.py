from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from apps.api.database import get_db
from apps.api.models import Image, Post
from packages.shared.auth import get_api_key

router = APIRouter(dependencies=[Depends(get_api_key)])

class ImageIndexRequest(BaseModel):
    filename: str
    url: str
    metadata_json: Dict[str, Any] = {}
    embeddings: List[float] = []

class RankResponseItem(BaseModel):
    image_id: int
    filename: str
    url: str
    score: float
    mismatch_reason: str = ""
    accepted: bool

@router.post("/index")
def index_image(img_req: ImageIndexRequest, db: Session = Depends(get_db)):
    db_img = Image(
        filename=img_req.filename,
        url=img_req.url,
        metadata_json=img_req.metadata_json,
        embeddings=img_req.embeddings
    )
    db.add(db_img)
    db.commit()
    db.refresh(db_img)
    return {"id": db_img.id, "status": "indexed"}

@router.post("/{post_id}/rank-images", response_model=List[RankResponseItem])
def rank_images(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    images = db.query(Image).all()
    
    # Fake ranking logic (since we don't have a real model here yet)
    # A real implementation would compute cosine similarity between post text embedding and image embeddings
    # and would also call the mismatch guard.
    
    results = []
    for idx, img in enumerate(images):
        # Fake score based on id just for testing
        score = 0.9 - (idx * 0.1)
        accepted = score >= 0.5
        mismatch_reason = "" if accepted else "Similarity confidence below threshold (0.5)"
        
        results.append(RankResponseItem(
            image_id=img.id,
            filename=img.filename,
            url=img.url,
            score=max(0.0, score),
            mismatch_reason=mismatch_reason,
            accepted=accepted
        ))
        
    # Sort by score descending
    results.sort(key=lambda x: x.score, reverse=True)
    return results
