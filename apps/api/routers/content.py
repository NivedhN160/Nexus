from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from apps.api.database import get_db
from apps.api.models import Post
from packages.shared.auth import get_api_key

router = APIRouter(dependencies=[Depends(get_api_key)])

class PostCreate(BaseModel):
    title: str
    body: str
    url: Optional[str] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    url: Optional[str] = None
    status: Optional[str] = None

class PostResponse(PostCreate):
    id: int
    status: str
    
    class Config:
        from_attributes = True

@router.post("", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(title=post.title, body=post.body, url=post.url, status="draft")
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("", response_model=List[PostResponse])
def get_posts(status: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(Post)
    if status:
        query = query.filter(Post.status == status)
    return query.offset(skip).limit(limit).all()

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.patch("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    update_data = post_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value)
        
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(post)
    db.commit()
    return {"ok": True}
