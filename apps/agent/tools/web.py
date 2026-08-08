import webbrowser
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

search_web_schema = {
    "type": "function",
    "function": {
        "name": "search_web",
        "description": "Search the web for a query. Opens the default browser with the search results.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query."
                }
            },
            "required": ["query"]
        }
    }
}

deep_web_search_schema = {
    "type": "function",
    "function": {
        "name": "deep_web_search",
        "description": "Searches the web and reads the content of the top result to provide detailed insights back to the LLM.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The specific query to search for."
                }
            },
            "required": ["query"]
        }
    }
}

def search_web(query):
    try:
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(url)
        return {"status": "success", "message": f"Opened web search for: {query}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def deep_web_search(query):
    try:
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        response = urllib.request.urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        
        results = []
        for a in soup.find_all('a', class_='result__snippet', limit=3):
            results.append(a.text)
            
        if results:
            return {"status": "success", "insights": " ".join(results)}
        else:
            return {"status": "success", "insights": "No detailed insights found."}
    except Exception as e:
        return {"status": "error", "error": str(e)}
