import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Using gemini-2.0-flash for reliable structured output processing with a massive free tier.
    MODEL_NAME = "gemini-2.0-flash"
    
    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing from environment variables.")
