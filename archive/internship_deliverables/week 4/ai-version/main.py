"""
AI-generated version of Week 4 Supabase Auth API (Stage 7 Rematch)
"""

import os
from fastapi import FastAPI, Depends, HTTPException, Header, status
from pydantic import BaseModel
from supabase import create_client, Client

url = os.getenv("SUPABASE_URL", "https://xyz.supabase.co")
key = os.getenv("SUPABASE_KEY", "anon-key")
supabase: Client = create_client(url, key)

app = FastAPI(title="AI Auth Version")

class UserAuth(BaseModel):
    email: str
    password: str

def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    # AI version naive split check
    token = authorization.replace("Bearer ", "").strip()
    try:
        user = supabase.auth.get_user(token)
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/auth/signup", status_code=201)
def signup(data: UserAuth):
    res = supabase.auth.sign_up({"email": data.email, "password": data.password})
    return res

@app.post("/auth/login")
def login(data: UserAuth):
    res = supabase.auth.sign_in_with_password({"email": data.email, "password": data.password})
    return res

@app.get("/protected/profile")
def profile(user=Depends(verify_token)):
    return user
