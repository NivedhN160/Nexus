# W5 — The Polite Scraper (Backend AI Engineering)

A production-ready, polite web scraping pipeline built in Python that respects `robots.txt`, identifies itself via custom `User-Agent` headers, enforces rate-limiting delays between HTTP requests, extracts structured data, and exports a clean JSON/CSV corpus ready for **Week 6 RAG (Retrieval-Augmented Generation)** indexing.

---

## 🏗️ Scraping Pipeline Architecture

```text
[ Target Website ]
        │
        ▼ 1. Fetch & Validate
[ robots.txt Rules ] ──▶ (Check Permission via RobotFileParser)
        │
        ▼ 2. Rate Limit (sleep 1.5s)
[ HTTP GET Request ] ──▶ (Identify via User-Agent Header)
        │
        ▼ 3. Extract & Clean
[ BeautifulSoup Parser ] ──▶ (Normalize Text & Extract Tags)
        │
        ▼ 4. Validate Schema
[ Pydantic Models ] ──▶ (QuoteItem & ScrapeResult)
        │
        ▼ 5. Export Corpus
┌───────┴───────┐
▼               ▼
data/*.json   data/*.csv (RAG Corpus Ready)
```

---

## 🤝 The 3 Pillars of Polite Bot Scraping

1. **Identification via User-Agent:**
   Every request sends a descriptive custom header identifying the bot and project repository:
   ```text
   User-Agent: FlyRankPoliteScraper/1.0 (+https://github.com/NivedhN160/flyrank-internship)
   ```
2. **Robots.txt Rule Compliance:**
   The scraper parses `https://quotes.toscrape.com/robots.txt` via `urllib.robotparser.RobotFileParser` before fetching any path. If a path is disallowed, the request is safely skipped.
3. **Rate Limiting & Backoff:**
   Enforces a mandatory **1.5-second delay (`time.sleep`)** between successive page requests to prevent server CPU or bandwidth spikes. Implements exponential backoff on HTTP 429 Rate Limit responses.

---

## 📁 Data Corpus Output Schema

Scraped records are validated using **Pydantic** (`models.py`) and saved to `data/scraped_quotes.json`:

```json
{
  "quote": "The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.",
  "author": "Albert Einstein",
  "author_url": "https://quotes.toscrape.com/author/Albert-Einstein",
  "tags": ["change", "deep-thoughts", "thinking", "world"]
}
```

---

## 🚀 Quickstart & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Polite Scraper
```bash
python main.py
```

### 3. Output Files Generated
* **JSON Corpus (For RAG Pipeline):** `week 5/data/scraped_quotes.json`
* **CSV Spreadsheet View:** `week 5/data/scraped_quotes.csv`

---

## 📝 Terminal Execution Log Snippet

```text
=== STARTING THE POLITE SCRAPER PIPELINE ===
User-Agent: FlyRankPoliteScraper/1.0 (+https://github.com/NivedhN160/flyrank-internship)
Target Site: https://quotes.toscrape.com/
Fetching robots.txt rules from: https://quotes.toscrape.com/robots.txt
Successfully loaded robots.txt for https://quotes.toscrape.com

--- Scraping Page 1/5: https://quotes.toscrape.com/ ---
Enforcing rate limit delay: sleeping for 1.50s...
Fetching URL: https://quotes.toscrape.com/
HTTP Status 200 for https://quotes.toscrape.com/ [Content Length: 11021 bytes]
Extracted 10 quote records from page. Next page: https://quotes.toscrape.com/page/2/

...

=== SCRAPING COMPLETE ===
Total Pages Scraped: 5
Total Records Extracted: 50
JSON export complete! 50 records written to data/scraped_quotes.json
CSV export complete! 50 rows written to data/scraped_quotes.csv
```
