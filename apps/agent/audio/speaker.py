from core.logger import setup_logger
logger = setup_logger(__name__)

import pyttsx3
import threading
import queue

# Create a queue for speech requests
speech_queue = queue.Queue()

def _tts_worker():
    # Initialize COM for Windows in the background thread
    import sys
    if sys.platform == 'win32':
        try:
            import pythoncom
            pythoncom.CoInitialize()
        except ImportError:
            pass
            
    # Initialize engine in the dedicated worker thread
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    
    while True:
        text = speech_queue.get()
        if text is None:
            break
        logger.info(f"NEOS (Voice): {text}")
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()

# Start the dedicated TTS thread
tts_thread = threading.Thread(target=_tts_worker, daemon=True)
tts_thread.start()

def speak(text):
    """Adds text to the speech queue in a non-blocking way."""
    if not text:
        return
    speech_queue.put(text)
