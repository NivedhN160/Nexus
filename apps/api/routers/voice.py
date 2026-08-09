from fastapi import APIRouter, Response, Depends
from pydantic import BaseModel
from packages.voice.tts import synthesize
from packages.shared.auth import get_api_key

router = APIRouter(dependencies=[Depends(get_api_key)])

class SynthesizeRequest(BaseModel):
    text: str

@router.post("/synthesize")
def synthesize_endpoint(req: SynthesizeRequest):
    try:
        audio_bytes = synthesize(req.text)
        return Response(content=audio_bytes, media_type="audio/wav")
    except Exception as e:
        # Degrade to empty response so it doesn't break chat clients expecting audio
        return Response(content=b'RIFF\x00\x00\x00\x00WAVE', media_type="audio/wav")
