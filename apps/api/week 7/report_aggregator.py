import json
import os
from collections import Counter
from typing import Dict, Any, List

class DataAggregator:
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path

    def load_data(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.json_file_path):
            # Fallback mock data if scraped_quotes.json is missing
            return [
                {"quote": "The world as we have created it is a process of our thinking.", "author": "Albert Einstein", "tags": ["change", "deep-thoughts", "thinking"]},
                {"quote": "It is our choices, Harry, that show what we truly are, far more than our abilities.", "author": "J.K. Rowling", "tags": ["abilities", "choices"]},
                {"quote": "There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.", "author": "Albert Einstein", "tags": ["inspirational", "life", "miracles"]},
                {"quote": "The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.", "author": "Jane Austen", "tags": ["aliteracy", "books", "classic", "humor"]}
            ]
        
        with open(self.json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # If wrapped in ScrapeResult format: {"quotes": [...]}
            if isinstance(data, dict) and "quotes" in data:
                return data["quotes"]
            elif isinstance(data, list):
                return data
            return []

    def generate_summary_metrics(self) -> Dict[str, Any]:
        quotes = self.load_data()
        total_quotes = len(quotes)
        
        authors = [q.get("author", "Unknown") for q in quotes]
        unique_authors = len(set(authors))
        author_counts = Counter(authors).most_common(5)
        
        all_tags = []
        for q in quotes:
            all_tags.extend(q.get("tags", []))
        
        tag_counts = Counter(all_tags).most_common(5)
        
        lengths = [len(q.get("quote", "")) for q in quotes]
        avg_length = round(sum(lengths) / total_quotes, 1) if total_quotes > 0 else 0

        return {
            "total_quotes": total_quotes,
            "unique_authors": unique_authors,
            "top_authors": author_counts,
            "top_tags": tag_counts,
            "avg_quote_length": avg_length,
            "sample_quotes": quotes[:6]
        }
