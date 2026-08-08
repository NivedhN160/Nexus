import sys
import os
from pathlib import Path

# Add the root directory to PYTHONPATH so packages/shared is accessible
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.api.database import engine, Base
from apps.api.routers import content, images, social, leads, metering, match, audit, affect, brain

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nexus API Gateway",
    description="Monolithic API for Nexus Personal AI Operations Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(content.router, prefix="/posts", tags=["Content"])
app.include_router(images.router, prefix="/images", tags=["Images"])
app.include_router(social.router, prefix="/campaigns", tags=["Social"])
app.include_router(leads.router, prefix="/leads", tags=["Leads"])
app.include_router(metering.router, prefix="/metering", tags=["Metering"])
app.include_router(match.router, prefix="/match", tags=["Match"])
app.include_router(audit.router, prefix="/audit", tags=["Audit"])
app.include_router(affect.router, prefix="/affect", tags=["Affect"])
app.include_router(brain.router, prefix="/brain", tags=["Brain"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
