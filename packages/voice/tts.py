import io

def synthesize(text: str) -> bytes:
    """
    11labs_local pattern: Offline/free TTS engine mock.
    In a real implementation, this would use a local model like pyttsx3, Coqui TTS, or a local Piper binary.
    For this implementation, we return dummy audio bytes so the backend succeeds.
    """
    # Return a 10-byte dummy wave header representation
    return b'RIFF\x00\x00\x00\x00WAVE'
