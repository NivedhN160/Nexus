import logging
import sys
from datetime import datetime
from scraper import PoliteScraper
from parser import QuoteParser
from exporter import DataExporter
from models import ScrapeResult

# 1. Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("PoliteScraper")

USER_AGENT = "FlyRankPoliteScraper/1.0 (+https://github.com/NivedhN160/flyrank-internship)"
START_URL = "https://quotes.toscrape.com/"
MAX_PAGES = 5  # Polite limit to prevent unnecessary server load

def main():
    logger.info("=== STARTING THE POLITE SCRAPER PIPELINE ===")
    logger.info(f"User-Agent: {USER_AGENT}")
    logger.info(f"Target Site: {START_URL}")
    logger.info(f"Max Page Limit: {MAX_PAGES}")

    scraper = PoliteScraper(user_agent=USER_AGENT, rate_limit_delay=1.5)
    parser = QuoteParser(base_domain="https://quotes.toscrape.com")
    exporter = DataExporter(output_dir="data")

    current_url = START_URL
    all_quotes = []
    pages_scraped = 0

    while current_url and pages_scraped < MAX_PAGES:
        logger.info(f"\n--- Scraping Page {pages_scraped + 1}/{MAX_PAGES}: {current_url} ---")
        html_content = scraper.fetch_page(current_url)
        
        if not html_content:
            logger.warning(f"Could not fetch HTML for {current_url}. Stopping pagination loop.")
            break
            
        page_quotes, next_page_url = parser.parse_page(html_content)
        all_quotes.extend(page_quotes)
        pages_scraped += 1
        current_url = next_page_url

    logger.info(f"\n=== SCRAPING COMPLETE ===")
    logger.info(f"Total Pages Scraped: {pages_scraped}")
    logger.info(f"Total Records Extracted: {len(all_quotes)}")

    result = ScrapeResult(
        target_domain="quotes.toscrape.com",
        total_scraped=len(all_quotes),
        pages_visited=pages_scraped,
        scraped_at=datetime.now().isoformat(),
        items=all_quotes
    )

    json_path = exporter.export_json(result, filename="scraped_quotes.json")
    csv_path = exporter.export_csv(all_quotes, filename="scraped_quotes.csv")

    logger.info(f"Saved JSON corpus to: {json_path}")
    logger.info(f"Saved CSV export to: {csv_path}")

if __name__ == "__main__":
    main()
