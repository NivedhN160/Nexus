import sys
import logging
import asyncio
from dotenv import load_dotenv

from .agent import DesktopAgent
from .config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    load_dotenv()
    
    if len(sys.argv) < 2:
        print("Usage: python -m src.main \"<your task description here>\"")
        sys.exit(1)
        
    task = " ".join(sys.argv[1:])
    
    try:
        agent = DesktopAgent()
        await agent.run(task)
    except Exception as e:
        logger.error(f"Agent terminated with error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
