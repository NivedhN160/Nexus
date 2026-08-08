# 🤖 CodePulse — DevOps & Backend API Verification Agent

> An autonomous Personal AI Agent powered by Model Context Protocol (MCP) live tools. CodePulse scans local backend software repositories, enforces `.env` secret isolation, executes subshell test suites, inspects web scraper politeness, and compiles Markdown audit reports.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/framework-FastAPI%20%7C%20MCP-orange.svg)](https://fastapi.tiangolo.com/)

---

## 🎯 1. Description & Job to be Done

### What CodePulse Does
CodePulse is a specialized personal AI agent built for software engineers and DevOps maintainers. It automates the tedious 30-minute manual code audit checklist on every new pull request:
1. **Secret Security Audit:** Verifies that `.env` files and unencrypted secrets are gitignored.
2. **Subshell Test Execution:** Runs isolated subshell test clients (`pytest`, `TestClient`) and parses exit codes.
3. **Web Scraper Politeness Verification:** Checks `robots.txt` compliance, rate-limiting delays, and User-Agent identification.
4. **Audit Report Compilation:** Generates structured Markdown reports with line-level code fix recommendations.

### Target Audience
Computer Science students, backend software engineers, and DevOps engineers maintaining FastAPI, PostgreSQL, Supabase Auth, or Web Scraping codebases.

---

## 🏗️ 2. Architecture & MCP Tool Engine

CodePulse is built on the **Model-Tools-Instructions Triad** specified in Anthropic and OpenAI agent design frameworks:

```text
                                  ┌────────────────────────────────┐
                                  │      CodePulse Agent Core      │
                                  │   (system_prompt.md + LLM)     │
                                  └───────────────┬────────────────┘
                                                  │
                ┌─────────────────────────────────┼─────────────────────────────────┐
                ▼                                 ▼                                 ▼
┌───────────────────────────────┐ ┌───────────────────────────────┐ ┌───────────────────────────────┐
│          `fs_reader`          │ │      `subshell_runner`       │ │    `http_polite_inspector`    │
│  Scans directories & .env     │ │  Executes pytest / PowerShell  │ │  Checks robots.txt compliance │
└───────────────┬───────────────┘ └───────────────┬───────────────┘ └───────────────┬───────────────┘
                │                                 │                                 │
                └─────────────────────────────────┼─────────────────────────────────┘
                                                  ▼
                                  ┌────────────────────────────────┐
                                  │        `report_writer`         │
                                  │  Writes audit_{subfolder}.md   │
                                  └────────────────────────────────┘
```

### Live MCP Tools Interface (`mcp_tools.py`)
* **`fs_reader(action, path)`:** Traverses local directory trees, inspects `.gitignore`, `.env.example`, and source code files.
* **`subshell_runner(command, cwd)`:** Spawns isolated PowerShell subshells to execute automated test suites (`pytest`, `test_endpoints.py`) and capture stdout/stderr.
* **`http_polite_inspector(url, user_agent)`:** Inspects target domain `robots.txt` rules and checks rate limiting delays.
* **`report_writer(target_path, content)`:** Writes structured Markdown audit reports directly to disk.

---

## 💻 3. Step-by-Step Setup Guide (Reproducible by a Stranger)

Follow these exact steps to set up and run CodePulse on any computer:

### Prerequisites
* **Python 3.10+** installed on your system (`python --version`).
* **Git** installed (`git --version`).

### Step 1: Clone the Repository
```bash
git clone https://github.com/NivedhN160/AI-Fluency-Capstone.git
cd AI-Fluency-Capstone
```

### Step 2: Create & Activate Virtual Environment
```bash
# On Windows PowerShell:
python -m venv venv
.\venv\Scripts\Activate.ps1

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

---

## 🚀 4. Usage Examples & CLI Commands

### Run Single Repository Audit
To audit a specific backend project subfolder:
```bash
python agent_runner.py
```
*Expected Output:*
```text
[CODEPULSE AGENT] STARTING AUDIT: Target Folder -> 'E:\Flyrank internship\week 6'
[STEP 1/4] Auditing Repository Secret Isolation (.env check)
[STEP 2/4] Executing Subshell Test Suite
[STEP 3/4] Inspecting Scraper Politeness & HTTP Status Specs
[STEP 4/4] Writing Audit Report Markdown Artifact
[SUCCESS] AUDIT REPORT SAVED TO: 'E:\Flyrank internship\ai fluency capstone\audit_reports\audit_week_6.md'
```

### Run Full 5-Eval Pre-Build Test Suite
To execute all 5 evaluation benchmarks sequentially:
```bash
python test_agent.py
```
*Expected Output:* `[SUCCESS] ALL 5 CAPSTONE EVAL CASES EXECUTED PERFECTLY!`

---

## 📊 5. Pre-Build Evaluation Results (5 Eval Cases)

| Eval Case | Target Track | Core Verification | Exit Code | Result |
| :--- | :--- | :--- | :--- | :--- |
| **Eval 1** | Week 2 (FastAPI CRUD API) | 9 REST endpoints verified; status codes enforced. | `0` | `100% PASS` |
| **Eval 2** | Week 3 (Postgres Docker) | `.env` isolated in `.gitignore`; Repository Pattern verified. | `0` | `100% PASS` |
| **Eval 3** | Week 4 (Supabase Auth API) | Bearer JWT token parsing & 401 unauthorized protection. | `0` | `100% PASS` |
| **Eval 4** | Week 6 (Async Job Queue) | HTTP 202 Accept Fast pattern, worker queue, retries & alerts. | `0` | `100% PASS` |
| **Eval 5** | Week 7 (PDF Report Generator) | Data aggregation engine & ReportLab binary PDF download. | `0` | `100% PASS` |

---

## 🛡️ 6. Safety Constraints & Guardrails

### ✋ Must Confirm (Human-in-the-Loop Gate)
The agent **MUST** prompt for explicit human approval before:
1. Executing `git push` to remote GitHub repositories.
2. Mutating existing production database tables.
3. Editing production secret keys in `.env`.

### 🚫 Must Never Do (Strict Prohibitions)
1. Never delete raw source code files (`rm -rf`).
2. Never commit unencrypted `.env` passwords to version control.
3. Never issue unthrottled HTTP request loops to external websites.

---

## ⚠️ 7. Limitations & Future Roadmap

### Current Limitations
1. **Local Subshell Scope:** CodePulse currently executes test suites in local PowerShell/Bash subshells rather than remote AWS EC2 SSH environments.
2. **Deterministic Test Discovery:** Relies on mapped test client scripts (`test_endpoints.py`) rather than dynamic LLM test generation.
3. **Synchronous Audit Queue:** Processes one repository folder per invocation loop.

### Future Roadmap (v2.0)
- [ ] Remote SSH Docker container test execution.
- [ ] Concurrent multi-repo parallel auditing worker.
- [ ] Automatic PR creation with inline GitHub code suggestions.

---

## 📄 License & Attribution

Built by **Nivedh** for the **FlyRank AI Internship — General AI Fluency Capstone**.  
Licensed under the [MIT License](LICENSE).
