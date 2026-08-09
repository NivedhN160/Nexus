import time
import os
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://nexus_user:nexus_password@localhost:5432/nexus_db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

from apps.api.models import Campaign, CampaignPost
from sqlalchemy.sql import func

def process_social_queue():
    # Poll database for queued campaigns that are due
    db = SessionLocal()
    try:
        # Find campaigns that are queued and run_at is in the past
        campaigns = db.query(Campaign).filter(
            Campaign.status == "queued",
            Campaign.run_at <= func.now()
        ).all()
        
        for campaign in campaigns:
            print(f"Worker: Processing campaign {campaign.id}")
            campaign.status = "published"
            for post in campaign.campaign_posts:
                post.status = "published"
                
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error processing social queue: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Nexus Worker started.")
    while True:
        try:
            process_social_queue()
        except Exception as e:
            print(f"Worker Error: {e}")
        time.sleep(5)
