import pyaudio
import numpy as np
from faster_whisper import WhisperModel
import speech_recognition as sr
import os
import logging
import wave

from core.logger import setup_logger
logger = setup_logger(__name__)

model_size = "base.en"
logger.info(f"Loading faster-whisper model ({model_size})...")
model = WhisperModel(model_size, device="cpu", compute_type="int8")

def listen_for_command():
    """
    Blocks and listens for speech using VAD.
    """
    
    # Listen for actual command
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1.2
    r.non_speaking_duration = 0.5
    
    with sr.Microphone() as source:
        logger.info("Recording command...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio_data = r.listen(source, timeout=5, phrase_time_limit=15)
            
            temp_file = "temp_audio.wav"
            with open(temp_file, "wb") as f:
                f.write(audio_data.get_wav_data())
                
            segments, info = model.transcribe(temp_file, beam_size=5)
            text = "".join([segment.text for segment in segments])
            
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
            return text.strip()
        except sr.WaitTimeoutError:
            logger.info("Listening timed out.")
            return ""
        except Exception as e:
            logger.error(f"Audio Error: {e}")
            return ""
