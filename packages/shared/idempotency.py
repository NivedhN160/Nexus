import redis
import os
import json
from functools import wraps
from fastapi import Request, HTTPException, status

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def idempotent(expire_seconds=86400):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            idempotency_key = request.headers.get("Idempotency-Key")
            if not idempotency_key:
                # If no key is provided, just proceed
                return await func(request, *args, **kwargs)
                
            redis_key = f"idempotency:{idempotency_key}"
            
            # Check if we already have a response
            cached_response = redis_client.get(redis_key)
            if cached_response:
                return json.loads(cached_response)
                
            # Execute the function
            response = await func(request, *args, **kwargs)
            
            # Store the response (assuming it's serializable to JSON/dict for FastAPI)
            if hasattr(response, 'dict'):
                response_data = response.dict()
            else:
                response_data = response
                
            redis_client.setex(redis_key, expire_seconds, json.dumps(response_data))
            
            return response
        return wrapper
    return decorator
