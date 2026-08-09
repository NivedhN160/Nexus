from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    api_key_hash = Column(String)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(Text)
    url = Column(String, nullable=True)
    status = Column(String, default="draft") # draft, imaged, scheduled, published, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    url = Column(String)
    metadata_json = Column(JSON, nullable=True)
    embeddings = Column(JSON, nullable=True) # Storing vector as JSON for simplicity, pgvector is better for production

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    run_at = Column(DateTime(timezone=True))
    status = Column(String, default="queued") # queued, publishing, published, failed
    
    post = relationship("Post")
    campaign_posts = relationship("CampaignPost", back_populates="campaign")

class CampaignPost(Base):
    __tablename__ = "campaign_posts"
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    platform = Column(String) # IG, X
    external_id = Column(String, nullable=True)
    status = Column(String, default="pending")
    caption = Column(Text)
    
    campaign = relationship("Campaign", back_populates="campaign_posts")

class Widget(Base):
    __tablename__ = "widgets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    config_json = Column(JSON)

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    widget_id = Column(Integer, ForeignKey("widgets.id"))
    name = Column(String)
    email = Column(String)
    message = Column(Text)
    geo = Column(String, nullable=True)
    status = Column(String, default="new")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MeteringEvent(Base):
    __tablename__ = "metering_events"
    id = Column(Integer, primary_key=True, index=True)
    idempotency_key = Column(String, unique=True, index=True)
    event_type = Column(String) # llm, vision
    cost_microcents = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MatchProfile(Base):
    __tablename__ = "match_profiles"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    tags = Column(JSON) # list of tags
    bio = Column(Text, nullable=True)
    embedding = Column(JSON, nullable=True) # Fake local embedding

class MatchThread(Base):
    __tablename__ = "match_threads"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="active") # active, confirmed, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    messages = relationship("MatchMessage", back_populates="thread")

class MatchMessage(Base):
    __tablename__ = "match_messages"
    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer, ForeignKey("match_threads.id"))
    sender = Column(String)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    thread = relationship("MatchThread", back_populates="messages")

class Thread(Base):
    __tablename__ = "threads"
    id = Column(String, primary_key=True, index=True) # UUID session_id
    title = Column(String, default="New Chat")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    messages = relationship("Message", back_populates="thread")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(String, ForeignKey("threads.id"))
    role = Column(String) # system, user, model, tool
    content = Column(Text, nullable=True)
    tool_calls = Column(JSON, nullable=True)
    tool_call_id = Column(String, nullable=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    thread = relationship("Thread", back_populates="messages")

class AuditReport(Base):
    __tablename__ = "audit_reports"
    id = Column(String, primary_key=True, index=True) # UUID report_id
    report_markdown = Column(Text)
    quality_score = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PendingApproval(Base):
    __tablename__ = "pending_approvals"
    id = Column(String, primary_key=True, index=True) # UUID
    tool_name = Column(String)
    arguments = Column(JSON)
    reason = Column(Text)
    status = Column(String, default="pending") # pending, approved, denied, executed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DecisionLog(Base):
    __tablename__ = "decision_logs"
    id = Column(Integer, primary_key=True, index=True)
    tool_name = Column(String)
    arguments = Column(JSON)
    level = Column(String)
    score = Column(Integer)
    reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MemoryChunk(Base):
    __tablename__ = "memory_chunks"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    tags = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
