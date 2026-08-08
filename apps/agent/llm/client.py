import yaml
import os
import time
from core.logger import setup_logger
from groq import Groq
from dotenv import load_dotenv

logger = setup_logger(__name__)

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
if not os.path.exists(config_path):
    raise FileNotFoundError("config.yaml is missing! Please create it from .env.example")

with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Load API keys from .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

_client = None

def get_client():
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            logger.error("GROQ_API_KEY not found in .env!")
            return None
        logger.info("Initializing Groq API Client...")
        _client = Groq(api_key=GROQ_API_KEY)
    return _client

def chat_with_tools(messages, tools=None):
    client = get_client()
    if client is None:
        return {"error": True, "details": "Groq client not initialized. Check API key."}

    try:
        sanitized_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if not isinstance(content, str):
                content = str(content)
                
            # Groq API doesn't accept "observation" role, map to user
            if role not in ["system", "user", "assistant"]:
                content = f"[{role.upper()}]: {content}"
                role = "user"
                
            sanitized_messages.append({
                "role": role,
                "content": content
            })

        kwargs = {
            "model": "llama-3.3-70b-versatile",
            "messages": sanitized_messages,
            "max_tokens": 1024,
            "temperature": 0.2
        }
        
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
            
        max_retries = 3
        delay = 1
        
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(**kwargs)
                choice = response.choices[0].message
                
                message_dict = {
                    "role": choice.role,
                    "content": choice.content
                }
                
                return {"message": message_dict}
            except Exception as e:
                logger.warning(f"LLM attempt {attempt+1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                else:
                    raise e
                    
    except Exception as e:
        import traceback
        return {"error": True, "details": f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"}
