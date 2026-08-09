# 🤖 FL-06: Personal AI Agent Design Specification

**Agent Name:** CodePulse — DevOps & Backend API Verification Agent  
**Track:** General AI Fluency (Week 5)  
**Deliverable:** 1-to-2 Page Technical Agent Design Specification  

---

## 🎯 1. Job to be Done & User Scope

### Job to be Done
CodePulse is a specialized personal AI agent designed to audit, test, and verify backend REST API repositories (FastAPI, PostgreSQL in Docker, Supabase Auth, and Web Scrapers). It scans repository file trees, verifies `.env` secret isolation, executes subshell test suites via MCP tools, audits `robots.txt` politeness compliance, and outputs structured markdown audit reports.

### Primary User & Usage Frequency
* **User:** Nivedh (Computer Science student & Backend Developer).
* **Usage Frequency:** Daily during local development and automated on every new Git pull request.
* **Estimated Build Scope:** ~10 build hours.

---

## 🛠️ 2. Tools & Data Sources Access Plan

| Tool Name | Tool Type | Access Plan & Connection Method | Function & Purpose |
| :--- | :--- | :--- | :--- |
| `fs_reader` | MCP File System Tool | Connected via local MCP `read_file` / `list_dir` server | Reads repository structure, `main.py`, `requirements.txt`, `.gitignore`, and `.env.example`. |
| `subshell_runner` | MCP Terminal Tool | Connected via local MCP `run_command` subshell execution | Runs `pytest`, `python test_w4_endpoints.py`, and `docker compose ps` verification. |
| `http_polite_inspector` | MCP Network Tool | Connected via `httpx` / `urllib` HTTP client | Inspects target domain `robots.txt` rules and checks live endpoint status codes (`201`, `204`, `401`). |

---

## 📝 3. Draft Instructions & Core Execution Loop

```text
You are CodePulse, a specialized DevOps and Backend API Verification Agent.

Your mission is to audit local backend codebases for correctness, security, and test compliance.

EXECUTION STEPS:
1. Scan the repository directory using fs_reader. Verify that .env is listed in .gitignore.
2. Read main.py, models.py, and requirements.txt to parse declared API endpoints.
3. Execute local test suites using subshell_runner (e.g. pytest or test_endpoints.py).
4. Parse raw subshell output. If any endpoint returns an incorrect status code (e.g. 200 instead of 201 Created), pinpoint the exact file and line number.
5. Generate a structured Markdown Audit Report highlighting:
   - Security Status (.env isolation)
   - Test Suite Pass/Fail Rate
   - Specific Code Fixes Required
```

---

## 🧪 4. Five Pre-Build Evaluation Cases (FL-03 Style)

### Eval Case 1: Clean Repository Audit
* **Input Repo:** `week 3/` (Postgres in Docker, `.env` gitignored, tests passing).
* **Expected Agent Action:** Runs subshell tests, confirms `.env` isolation.
* **Expected Output:** `Status: 100% PASS`. Zero security flags raised.

### Eval Case 2: Exposed Secret Security Alert
* **Input Repo:** A project where `.env` is missing from `.gitignore`.
* **Expected Agent Action:** Detects `.env` in git status.
* **Expected Output:** `Status: CRITICAL SECURITY ALERT`. Generates immediate `.gitignore` patch snippet and flags exposed API keys.

### Eval Case 3: HTTP Status Code Mismatch
* **Input Repo:** `POST /tasks` endpoint returning `200 OK` instead of `201 Created`.
* **Expected Agent Action:** Parses test output, identifies status code discrepancy in `main.py`.
* **Expected Output:** `Status: SPEC VIOLATION`. Highlights line number in `main.py` and proposes `status_code=status.HTTP_201_CREATED` fix.

### Eval Case 4: Impolite Scraper Politeness Alert
* **Input Repo:** Web scraper missing rate-limiting delay or custom `User-Agent`.
* **Expected Agent Action:** Inspects `scraper.py`, notices missing `time.sleep` or missing `robots.txt` check.
* **Expected Output:** `Status: POLITENESS VIOLATION`. Recommends inserting `PoliteChecker` wrapper and User-Agent identification header.

### Eval Case 5: Missing Bearer Token Protection
* **Input Repo:** Protected route `/protected/profile` accessible without `Authorization: Bearer` header.
* **Expected Agent Action:** Executes test call without header, receives `200 OK` instead of `401 Unauthorized`.
* **Expected Output:** `Status: AUTH SECURITY GAP`. Flags missing `Depends(get_current_user)` dependency in `main.py`.

---

## 🛡️ 5. Risks and Guardrails Design

### ✋ Must Confirm (Human-in-the-Loop Gate)
The agent **MUST** prompt for explicit human approval before:
1. Pushing commits or tags to remote GitHub repositories (`git push`).
2. Overwriting or mutating existing database files (`tasks.db` or PostgreSQL tables).
3. Modifying production environment variable values in `.env`.

### 🚫 Must Never Do (Strict Prohibitions)
The agent is **STRICTLY PROHIBITED** from:
1. Deleting raw source code files or directory structures (`rm -rf` or file deletion).
2. Committing `.env` secret keys or private passwords to public Git repositories.
3. Sending unthrottled HTTP requests to external websites without rate limiting.

---

## 🏛️ 6. Platform Choice & Justification

* **Selected Platform:** **Claude AI Workspace / Antigravity Agent with Local MCP Connectors.**
* **Alternative Considered:** *n8n Cloud Workflow / Custom GPT.*
* **Justification:**  
  Claude Workspace equipped with local MCP connectors (`run_command`, `read_file`) provides direct, low-latency access to local subshell test execution and NTFS directory traversal. Custom GPTs lack native local subshell execution capabilities and require paid API subscriptions, whereas n8n cloud workflows require complex webhook setup for local code execution.

---

## 🔄 Pass / Revise Checklist
* [x] **Realistic ~10 Hour Scope:** Focused tightly on backend API auditing and test execution.
* [x] **Realistic Tool Access Plan:** `fs_reader`, `subshell_runner`, and `http_polite_inspector` connected via MCP.
* [x] **Five Pre-Build Eval Cases:** Defined expected actions and outputs for clean repos, secret leaks, status mismatches, scraper violations, and auth gaps.
* [x] **Specified Guardrails:** Explicit human-in-the-loop gates and forbidden actions.
* [x] **Platform Justified:** Justified Claude AI Workspace with MCP connectors over n8n and Custom GPTs.
