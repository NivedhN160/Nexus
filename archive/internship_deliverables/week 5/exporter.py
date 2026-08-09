import os
import json
import csv
import logging
from typing import List
from models import ScrapeResult, QuoteItem

logger = logging.getLogger("PoliteScraper")

class DataExporter:
    def __init__(self, output_dir: str = "data"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export_json(self, result: ScrapeResult, filename: str = "scraped_quotes.json") -> str:
        filepath = os.path.join(self.output_dir, filename)
        logger.info(f"Saving structured JSON corpus to: {filepath}")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result.model_dump(), f, indent=2, ensure_ascii=False)
        logger.info(f"JSON export complete! {result.total_scraped} records written.")
        return filepath

    def export_csv(self, items: List[QuoteItem], filename: str = "scraped_quotes.csv") -> str:
        filepath = os.path.join(self.output_dir, filename)
        logger.info(f"Saving CSV spreadsheet view to: {filepath}")
        fieldnames = ["quote", "author", "author_url", "tags"]
        
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                writer.writerow({
                    "quote": item.quote,
                    "author": item.author,
                    "author_url": item.author_url or "",
                    "tags": ", ".join(item.tags)
                })
        logger.info(f"CSV export complete! {len(items)} rows written.")
        return filepath
