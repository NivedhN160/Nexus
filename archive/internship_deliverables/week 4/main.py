import os
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any
from fastapi import FastAPI, Request, Response, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-supabase-anon-key")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
security_bearer = HTTPBearer(
    auto_error=False,
    description="Enter your Supabase JWT access_token obtained from /auth/login"
)

class AuthCredentials(BaseModel):
    email: str = Field(..., example="user@example.com", description="User email address")
    password: str = Field(..., example="password123", description="User account password")

async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer)) -> Dict[str, Any]:
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Access token required"}
        )
    token = credentials.credentials.strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Access token required"}
        )
    
    try:
        user_response = supabase.auth.get_user(token)
        user = user_response.user
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Invalid or expired token"}
            )
        return {
            "id": user.id,
            "email": user.email,
            "created_at": str(user.created_at) if hasattr(user, "created_at") else None,
            "role": getattr(user, "role", "authenticated"),
            "token": token
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid or expired token"}
        )

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server running and connected to Supabase")
    yield

app = FastAPI(
    title="Auth API (Supabase Auth & Bearer JWT Protection)",
    description="A secure FastAPI authentication service integrated with Supabase Auth as Identity Provider (IdP). Features Bearer JWT token verification, public/protected routes, reusable auth dependencies, and interactive Swagger UI authorization.",
    version="1.0.0",
    lifespan=lifespan
)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.get(
    "/",
    summary="Root API Information",
    description="Returns metadata about the Auth API service."
)
def read_root():
    return {"message": "Auth API Server running and connected to Supabase"}

@app.get(
    "/public/info",
    summary="Public Information Endpoint",
    description="Public, unprotected route accessible to all strangers without authentication."
)
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@app.get(
    "/protected/profile",
    summary="User Profile Endpoint (Protected)",
    description="Protected route requiring a valid Bearer JWT. Decodes and verifies token via Supabase Auth and returns user metadata."
)
def protected_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "created_at": current_user["created_at"],
        "role": current_user["role"]
    }

@app.get(
    "/protected/dashboard",
    summary="User Dashboard Endpoint (Protected)",
    description="Second protected route demonstrating reusable auth middleware protection across endpoints."
)
def protected_dashboard(current_user: Dict[str, Any] = Depends(get_current_user)):
    return {
        "message": f"Welcome to your private dashboard, {current_user['email']}!",
        "metrics": {
            "account_status": "Active",
            "access_level": current_user["role"],
            "session_valid": True
        }
    }

@app.post(
    "/auth/signup",
    status_code=status.HTTP_201_CREATED,
    summary="Sign Up New Account",
    description="Registers a new user account with Supabase Auth. Requires non-empty email and password."
)
async def signup(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid or missing JSON body"}
        )
    
    if not isinstance(data, dict):
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must be a JSON object"}
        )
        
    email = data.get("email")
    password = data.get("password")
    
    if not email or not isinstance(email, str) or not email.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Email is required"}
        )
    if not password or not isinstance(password, str) or not password.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Password is required"}
        )

    try:
        response = supabase.auth.sign_up({
            "email": email.strip(),
            "password": password.strip()
        })
        user = response.user
        user_data = {
            "id": user.id if user else None,
            "email": user.email if user else email.strip(),
            "created_at": str(user.created_at) if user and hasattr(user, "created_at") else None
        }
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "User registered successfully", "user": user_data}
        )
    except Exception as e:
        error_msg = str(e)
        return JSONResponse(
            status_code=400,
            content={"error": error_msg}
        )

@app.post(
    "/auth/login",
    summary="Log In & Issue JWT",
    description="Authenticates credentials with Supabase Auth. Returns JWT access_token and refresh_token on success."
)
async def login(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid or missing JSON body"}
        )
        
    if not isinstance(data, dict):
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must be a JSON object"}
        )

    email = data.get("email")
    password = data.get("password")
    
    if not email or not isinstance(email, str) or not email.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required"}
        )
    if not password or not isinstance(password, str) or not password.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required"}
        )

    try:
        response = supabase.auth.sign_in_with_password({
            "email": email.strip(),
            "password": password.strip()
        })
        session = response.session
        user = response.user
        
        if not session or not session.access_token:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid login credentials"}
            )
            
        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id if user else None,
                "email": user.email if user else email.strip()
            }
        }
    except Exception:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid login credentials"}
        )

@app.post(
    "/auth/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Log Out User Session (Protected)",
    description="Revokes current user session via Supabase Auth. Requires valid Bearer JWT token."
)
def logout(current_user: Dict[str, Any] = Depends(get_current_user)):
    try:
        supabase.auth.sign_out(current_user["token"])
    except Exception:
        pass
    return Response(status_code=status.HTTP_204_NO_CONTENT)
