import logging
from typing import List, Tuple, Optional
from bs4 import BeautifulSoup
from models import QuoteItem

logger = logging.getLogger("PoliteScraper")

class QuoteParser:
    def __init__(self, base_domain: str = "https://quotes.toscrape.com"):
        self.base_domain = base_domain

    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        # Remove smart quotes and normalize whitespace
        cleaned = text.strip().replace("“", "").replace("”", "").replace('"', '')
        return " ".join(cleaned.split())

    def parse_page(self, html_content: str) -> Tuple[List[QuoteItem], Optional[str]]:
        soup = BeautifulSoup(html_content, "html.parser")
        quote_elements = soup.find_all("div", class_="quote")
        items: List[QuoteItem] = []

        for q in quote_elements:
            # Extract quote text
            text_el = q.find("span", class_="text")
            raw_text = text_el.get_text() if text_el else ""
            cleaned_quote = self.clean_text(raw_text)

            # Extract author
            author_el = q.find("small", class_="author")
            author_name = author_el.get_text().strip() if author_el else "Unknown"

            # Extract author URL link
            author_link_el = q.find("a", href=True)
            author_url = None
            if author_link_el and author_link_el["href"].startswith("/author/"):
                author_url = f"{self.base_domain}{author_link_el['href']}"

            # Extract tags
            tag_elements = q.find_all("a", class_="tag")
            tags = [t.get_text().strip() for t in tag_elements if t.get_text()]

            if cleaned_quote:
                items.append(QuoteItem(
                    quote=cleaned_quote,
                    author=author_name,
                    author_url=author_url,
                    tags=tags
                ))

        # Extract next page pagination link
        next_li = soup.find("li", class_="next")
        next_page_url = None
        if next_li and next_li.find("a", href=True):
            relative_href = next_li.find("a")["href"]
            next_page_url = f"{self.base_domain}{relative_href}"

        logger.info(f"Extracted {len(items)} quote records from page. Next page: {next_page_url}")
        return items, next_page_url
