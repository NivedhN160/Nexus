import urllib.request
import json
import base64
import os
import re
from datetime import datetime, timezone

# Load .env file natively if it exists
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, val = line.strip().split("=", 1)
                os.environ[key.strip()] = val.strip().strip('"').strip("'")

USERNAME = "NivedhN160"
GH_PAT = os.environ.get("GH_PAT")

def fetch_repos():
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GH_PAT:
        headers["Authorization"] = f"token {GH_PAT}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching repos: {e}")
        return []

def fetch_readme(repo_name):
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/readme"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GH_PAT:
        headers["Authorization"] = f"token {GH_PAT}"
        
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return base64.b64decode(data['content']).decode('utf-8', errors='ignore')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "" # No README
        print(f"Error fetching README for {repo_name}: {e}")
        return ""
    except Exception as e:
        print(f"Error fetching README for {repo_name}: {e}")
        return ""

def score_readme(readme, pushed_at_str):
    if not readme:
        return 0

    score = 0
    words = readme.split()
    word_count = len(words)
    
    # word count > 150
    if word_count > 150:
        score += 10
        
    # has intro paragraph
    first_200 = " ".join(words[:200])
    if "." in first_200 and len(words) > 20:
        score += 10
        
    # code block count
    code_blocks = readme.count("```")
    score += min(code_blocks * 3, 15)
    
    # architecture / diagram
    if re.search(r'(architecture|diagram|mermaid)', readme, re.IGNORECASE):
        score += 15
        
    # usage / install
    if re.search(r'(install|usage|getting started)', readme, re.IGNORECASE):
        score += 10
        
    # live demo
    if re.search(r'(demo|try it|live)', readme, re.IGNORECASE):
        score += 20
        
    # recency
    try:
        # pushed_at format: 2026-06-20T12:00:00Z
        pushed_at = datetime.strptime(pushed_at_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        days_since = (now - pushed_at).days
        if days_since < 30:
            score += 10
    except:
        pass
        
    # header count
    headers = len(re.findall(r'^#{2,3}\s', readme, re.MULTILINE))
    score += min(headers * 2, 10)
    
    return score

def main():
    repos = fetch_repos()
    if not repos:
        print("No repos found or error occurred.")
        return
        
    projects = []
    
    for repo in repos:
        if repo['fork']:
            continue # Skip forks
            
        print(f"Processing {repo['name']}...")
        readme = fetch_readme(repo['name'])
        score = score_readme(readme, repo['pushed_at'])
        
        projects.append({
            "name": repo['name'],
            "description": repo['description'] or "",
            "url": repo['html_url'],
            "language": repo['language'] or "Unknown",
            "score": score,
            "last_updated": repo['pushed_at'],
            "homepage": repo['homepage'] or ""
        })
        
    projects.sort(key=lambda x: x['score'], reverse=True)
    
    featured = projects[0]['name'] if projects else ""
    
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "featured": featured,
        "projects": projects
    }
    
    with open("projects.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
        
    print(f"Successfully generated projects.json. Featured project: {featured}")

if __name__ == "__main__":
    main()
