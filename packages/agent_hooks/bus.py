import json
import logging
from typing import Dict, Any, Callable, List

logger = logging.getLogger(__name__)

class EventBus:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        
    def subscribe(self, event_type: str, callback: Callable[[Dict[str, Any]], None]):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
        
    def emit(self, event_type: str, payload: Dict[str, Any]):
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                try:
                    callback(payload)
                except Exception as e:
                    logger.error(f"Error in event listener for {event_type}: {e}")

# Global singleton
bus = EventBus()
