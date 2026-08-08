from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from typing import Dict, List, Optional
from openai import AsyncOpenAI
from starlette.middleware.cors import CORSMiddleware
import httpx
import uvicorn
import traceback

# Load environment variables
load_dotenv()

app = FastAPI(title="TERRA-X Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI Client Initialization
def get_ai_client():
    groq_key = (os.getenv("GROQ_API_KEY") or "").strip()
    openai_key = (os.getenv("OPENAI_API_KEY") or "").strip()
    
    # Priority 1: Groq (Llama-3.3 - Fast & Free)
    if groq_key and groq_key.startswith("gsk_"):
        masked = groq_key[:6] + "..." + groq_key[-4:]
        print(f"INFO: Initializing Groq Client (Key: {masked})")
        # Using Llama 3.3 70B for better analysis, fallback to 8B if needed
        return AsyncOpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1"), "llama-3.3-70b-versatile"
    
    # Priority 2: OpenAI (GPT-3.5)
    if openai_key and openai_key.startswith("sk-"):
        masked = openai_key[:6] + "..." + openai_key[-4:]
        print(f"INFO: Initializing OpenAI Client (Key: {masked})")
        return AsyncOpenAI(api_key=openai_key), "gpt-3.5-turbo"
        
    print("CRITICAL: No valid AI keys found in .env")
    return None, None

ai_client, MODEL = get_ai_client()
WEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

class SimulationRequest(BaseModel):
    location: str
    lat: float
    lon: float
    carbon_change: int
    pop_growth: int
    econ_shift: int
    resource_use: int

@app.get("/health")
async def health():
    return {
        "status": "online", 
        "ai_active": ai_client is not None,
        "engine": MODEL if ai_client else "NONE",
        "weather_active": bool(WEATHER_KEY)
    }

async def get_real_weather(lat, lon):
    if not WEATHER_KEY:
        return None
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_KEY}&units=metric"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=5.0)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "temp": data['main']['temp'],
                    "desc": data['weather'][0]['description'],
                    "humidity": data['main']['humidity']
                }
    except Exception as e:
        print(f"Weather error: {e}")
    return None

@app.post("/api/simulate")
async def run_scenario_simulation(req: SimulationRequest):
    global ai_client, MODEL
    
    # Re-init if client is missing (allows .env updates without full restart in some envs)
    if not ai_client:
        ai_client, MODEL = get_ai_client()

    if not ai_client:
        raise HTTPException(status_code=503, detail="AI Simulation Engine Offline. Please check your GROQ_API_KEY in .env")
    
    real_weather = await get_real_weather(req.lat, req.lon)
    weather_context = ""
    if real_weather:
        weather_context = f"\nREAL-TIME BASELINE for {req.location}: Temp {real_weather['temp']}C, {real_weather['desc']}"

    prompt = f"""Analyze this planetary simulation for {req.location}.
    {weather_context}
    
    CHANG_VARS:
    - CO2: {req.carbon_change}%
    - Pop: {req.pop_growth}%
    - Econ: {req.econ_shift}%
    - Resources: {req.resource_use}%
    
    TASK:
    1. Predict the outcome in plain language.
    2. Respond as a professional Intelligence Engine.
    3. Max 50 words.
    4. Format: One paragraph prediction + one 'STRATEGIC ADVICE' sentence."""

    try:
        response = await ai_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are the TERRA-X Simulation Oracle. Ground your output in realistic atmospheric science."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=250
        )
        return {
            "analysis": response.choices[0].message.content.strip(),
            "baseline": real_weather
        }
    except Exception as e:
        err_str = str(e)
        print(f"AI ERROR: {err_str}")
        
        # If the 70b fail, try the 8b as a last resort
        if "llama-3.3" in MODEL:
            try:
                print("INFO: Falling back to Llama-3-8B...")
                fallback_resp = await ai_client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=250
                )
                return {
                    "analysis": fallback_resp.choices[0].message.content.strip(),
                    "baseline": real_weather
                }
            except:
                pass

        raise HTTPException(status_code=500, detail=f"Simulation Engine Error: {err_str[:150]}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
