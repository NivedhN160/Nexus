from fastapi import APIRouter, Depends
from pydantic import BaseModel
from packages.shared.auth import get_api_key
from packages.presence.mock_provider import mock_presence
import os
import random
from groq import Groq

router = APIRouter(dependencies=[Depends(get_api_key)])

class PresenceUpdate(BaseModel):
    is_present: bool

@router.get("/presence")
def get_presence():
    return {"status": "success", "context": mock_presence.get_context(), "is_present": mock_presence.is_present}

@router.post("/presence")
def update_presence(req: PresenceUpdate):
    mock_presence.set_presence(req.is_present)
    return {"status": "success"}

class SimulationRequest(BaseModel):
    location: str
    carbon_change: int
    pop_growth: int
    econ_shift: int
    resource_use: int

@router.post("/terra-x/simulate")
def run_terra_x_simulation(req: SimulationRequest):
    weather_desc = random.choice(["Clear sky", "Light rain", "Overcast", "Scattered clouds"])
    temp = random.randint(15, 35)
    
    prompt = f"Analyze planetary simulation for {req.location}. Weather: {temp}C, {weather_desc}. CO2: {req.carbon_change}%, Pop: {req.pop_growth}%, Econ: {req.econ_shift}%, Res: {req.resource_use}%. Max 50 words prediction and strategic advice."
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key or os.getenv("NEXUS_CLOUD_LLM", "0") != "1":
        analysis = f"[Local Simulation] Due to carbon change of {req.carbon_change}% and resource usage of {req.resource_use}%, {req.location} will experience shifts in microclimates over the next decade. STRATEGIC ADVICE: Stabilize resource consumption immediately."
    else:
        try:
            client = Groq(api_key=groq_api_key)
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            analysis = resp.choices[0].message.content
        except Exception as e:
            analysis = f"Simulation failed: {str(e)}"
            
    return {
        "analysis": analysis,
        "baseline": {"temp": temp, "desc": weather_desc, "humidity": random.randint(40, 90)}
    }

class StockAnalyzeRequest(BaseModel):
    ticker: str

@router.post("/stock/analyze")
def analyze_stock(req: StockAnalyzeRequest):
    price = round(random.uniform(50.0, 500.0), 2)
    change = round(random.uniform(-5.0, 5.0), 2)
    volume = random.randint(10000, 10000000)
    
    prompt = f"Analyze stock {req.ticker}. Current price: ${price}, Change: {change}%, Volume: {volume}. Max 50 words technical and fundamental brief."
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key or os.getenv("NEXUS_CLOUD_LLM", "0") != "1":
        direction = "bullish" if change > 0 else "bearish"
        analysis = f"[Local Analysis] {req.ticker} is currently showing {direction} momentum with a recent {change}% change. Given the volume of {volume}, institutional support is likely present. Consider waiting for confirmation before entry."
    else:
        try:
            client = Groq(api_key=groq_api_key)
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            analysis = resp.choices[0].message.content
        except Exception as e:
            analysis = f"Analysis failed: {str(e)}"
            
    return {
        "analysis": analysis,
        "market_data": {"price": price, "change": change, "volume": volume}
    }
