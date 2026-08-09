import logging
import requests
from typing import Optional
from polite_checker import PoliteChecker

logger = logging.getLogger("PoliteScraper")

class PoliteScraper:
    def __init__(self, user_agent: str, rate_limit_delay: float = 1.5):
        self.user_agent = user_agent
        self.polite_checker = PoliteChecker(user_agent=user_agent, default_delay=rate_limit_delay)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        })

    def fetch_page(self, url: str) -> Optional[str]:
        # 1. Check robots.txt permissions
        if not self.polite_checker.is_allowed(url):
            logger.error(f"Skipping {url} — disallowed by robots.txt rules.")
            return None

        # 2. Enforce polite rate limit delay
        self.polite_checker.enforce_rate_limit()

        # 3. Execute HTTP GET request
        try:
            logger.info(f"Fetching URL: {url}")
            response = self.session.get(url, timeout=10)
            logger.info(f"HTTP Status {response.status_code} for {url} [Content Length: {len(response.text)} bytes]")
            
            if response.status_code == 200:
                return response.text
            elif response.status_code == 429:
                logger.warning(f"Rate limited (HTTP 429) on {url}. Applying exponential backoff...")
                self.polite_checker.enforce_rate_limit(delay=5.0)
                return self.fetch_page(url)
            else:
                logger.error(f"Failed to fetch {url} — HTTP Status {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Network error fetching {url}: {e}")
            return None
