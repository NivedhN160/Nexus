from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class QuoteItem(BaseModel):
    quote: str = Field(..., description="Cleaned text of the quote")
    author: str = Field(..., description="Author of the quote")
    author_url: Optional[str] = Field(None, description="Absolute URL to author profile")
    tags: List[str] = Field(default_factory=list, description="Categorized tags")

class ScrapeResult(BaseModel):
    target_domain: str
    total_scraped: int
    pages_visited: int
    scraped_at: str
    items: List[QuoteItem]
