import logging
import time
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

logger = logging.getLogger("PoliteScraper")

class PoliteChecker:
    def __init__(self, user_agent: str, default_delay: float = 1.5):
        self.user_agent = user_agent
        self.default_delay = default_delay
        self.parsers = {}

    def get_robot_parser(self, base_url: str) -> RobotFileParser:
        parsed = urlparse(base_url)
        domain = f"{parsed.scheme}://{parsed.netloc}"
        
        if domain not in self.parsers:
            robots_url = f"{domain}/robots.txt"
            logger.info(f"Fetching robots.txt rules from: {robots_url}")
            parser = RobotFileParser()
            parser.set_url(robots_url)
            try:
                parser.read()
                logger.info(f"Successfully loaded robots.txt for {domain}")
            except Exception as e:
                logger.warning(f"Could not fetch robots.txt for {domain} ({e}). Assuming standard access.")
            self.parsers[domain] = parser
            
        return self.parsers[domain]

    def is_allowed(self, url: str) -> bool:
        parser = self.get_robot_parser(url)
        allowed = parser.can_fetch(self.user_agent, url)
        if not allowed:
            logger.warning(f"BLOCKED BY ROBOTS.TXT: {url}")
        return allowed

    def enforce_rate_limit(self, delay: float = None):
        wait_time = delay if delay is not None else self.default_delay
        logger.info(f"Enforcing rate limit delay: sleeping for {wait_time:.2f}s...")
        time.sleep(wait_time)
