import redis
import os
from contextlib import contextmanager

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

class IdempotencyConflictException(Exception):
    pass

@contextmanager
def idempotency_lock(key: str, ttl_seconds: int = 3600):
    """
    Ensures that a block of code is only executed once for a given key within the TTL.
    Used for webhooks and duplicated submissions.
    """
    lock_key = f"nexus:idemp:{key}"
    
    # Try to acquire the lock (SETNX)
    acquired = redis_client.set(lock_key, "locked", nx=True, ex=ttl_seconds)
    
    if not acquired:
        raise IdempotencyConflictException(f"Request with idempotency key {key} is already being processed or was processed recently.")
    
    try:
        yield
    except Exception:
        # If the block fails, we release the lock so it can be retried
        redis_client.delete(lock_key)
        raise
