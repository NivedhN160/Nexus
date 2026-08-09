from pydantic import BaseModel
from typing import Literal

class Budget(BaseModel):
    max_cost: float = 0.0
    max_tokens: int = 100000
    reserve: int = 1000
    exceed_policy: Literal['WARN', 'STOP'] = 'STOP'
    
    current_cost: float = 0.0
    current_tokens: int = 0
    
    def can_afford(self, estimated_tokens: int = 0) -> bool:
        if self.current_tokens + estimated_tokens > self.max_tokens:
            return False
        return True

    def record(self, tokens: int, cost: float = 0.0):
        self.current_tokens += tokens
        self.current_cost += cost

    def check_and_record(self, tokens: int, cost: float = 0.0) -> bool:
        if not self.can_afford(tokens):
            return False
        self.record(tokens, cost)
        return True
