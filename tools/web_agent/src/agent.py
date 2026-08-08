import asyncio
import logging
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import Field
from .config import Config

logger = logging.getLogger(__name__)

class PatchedGoogleGenAI(ChatGoogleGenerativeAI):
    """
    Patched model to bypass browser-use v0.13.6 telemetry bug where it assumes
    the model has 'provider' and 'model_name' attributes.
    """
    provider: str = Field(default="google")
    model_name: str = Field(default="gemini-2.0-flash")

class DesktopAgent:
    """The Browser Agent using Playwright and browser-use."""
    
    def __init__(self):
        Config.validate()
        self.llm = PatchedGoogleGenAI(
            model=Config.MODEL_NAME, 
            api_key=Config.GEMINI_API_KEY
        )

    async def run(self, task: str):
        """Runs the task in the browser."""
        logger.info(f"Starting Browser Agent for task: '{task}'")
        agent = Agent(task=task, llm=self.llm)
        await agent.run()
