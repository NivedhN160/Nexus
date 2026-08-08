# 📹 FL-09: Capstone Documentation & Demo Video Deliverable

**Track:** General AI Fluency (Week 8)  
**Deliverable:** Reproducible Capstone README & 5-Minute Live Screen Recording Script  
**Capstone GitHub Repository:** [https://github.com/NivedhN160/AI-Fluency-Capstone](https://github.com/NivedhN160/AI-Fluency-Capstone)  
**Capstone Live Showcase:** [https://ai-fluency-capstone.netlify.app](https://ai-fluency-capstone.netlify.app)  

---

## 📄 Section 1: Stranger-Reproducible README Breakdown

The primary documentation artifact for the `CodePulse` AI Agent is published in the root of the dedicated repository at **`https://github.com/NivedhN160/AI-Fluency-Capstone/blob/main/README.md`**.

### Key Sections Covered:
1. **Description & Job to be Done:** Explains how CodePulse automates code reviews, secret scanning, subshell test suite execution, and scraper politeness auditing.
2. **Architecture & MCP Tool Engine:** Features an ASCII architecture diagram mapping `fs_reader`, `subshell_runner`, `http_polite_inspector`, and `report_writer`.
3. **Step-by-Step Setup Guide:** Gives exact, unambiguous commands (`git clone`, `python -m venv venv`, `pip install -r requirements.txt`, `cp .env.example .env`) so a stranger can reproduce the entire setup from scratch.
4. **Pre-Build Evaluation Results:** Documents pass/fail status and exit codes for all 5 pre-build evals.
5. **Guardrails & Safety Constraints:** Highlights human-in-the-loop confirmation gates (`git push`, DB mutations) and forbidden actions (`rm -rf`, committing `.env` passwords).
6. **Limitations & Roadmap:** Honestly states current limitations (local subshell execution vs. remote cloud SSH) and future v2.0 roadmap items.

---

## 🎙️ Section 2: Live Demo Video Script & Recording Guide (3 to 5 Minutes)

Use this step-by-step narration script when recording your screen with **OBS Studio**, **Loom**, or **Windows Game Bar (Win + Alt + R)**.

### ⏱️ Timestamped Video Script

#### `0:00 - 0:45` | Introduction & Purpose
* **Screen Visual:** Browser open to `https://ai-fluency-capstone.netlify.app` showcasing the hero banner and live Agent Console.
* **Narration Script:**  
  > *"Hi everyone, my name is Nivedh, and today I'm demonstrating CodePulse—an autonomous DevOps and Backend API Verification Agent built for my General AI Fluency Capstone. In backend engineering, auditing pull requests manually takes 30 minutes per release—checking .env security, running test suites, verifying scrapers, and writing reports. CodePulse automates this entire checklist in under 10 seconds using Model Context Protocol tools."*

#### `0:45 - 2:00` | Live End-to-End Agent Run
* **Screen Visual:** Switch to PowerShell terminal in VS Code. Type `python test_agent.py` and press Enter.
* **Narration Script:**  
  > *"Let's run a live end-to-end audit across my 5 pre-build eval benchmarks. As you can see on screen, CodePulse starts by scanning directory trees with `fs_reader` to verify that `.env` files are gitignored. Next, `subshell_runner` spawns isolated PowerShell instances to execute pytest suites. Then `http_polite_inspector` checks robots.txt rules, and `report_writer` compiles the Markdown artifact. All 5 evals—FastAPI CRUD, Postgres Docker, Supabase Auth, Async Job Worker, and PDF Generator—have executed with 100% pass rate."*

#### `2:00 - 3:15` | Explaining One Key Design Decision (On Camera)
* **Screen Visual:** Open `mcp_tools.py` in VS Code and highlight lines 32–48 (`subshell_runner` implementation).
* **Narration Script:**  
  > *"A critical design decision in CodePulse is decoupling LLM prompt generation from actual code execution. Instead of letting the LLM execute arbitrary terminal strings directly, I built a dedicated MCP tool contract called `subshell_runner`. The agent can request test execution, but the tool enforces a strict 30-second timeout, captures stdout/stderr in isolated buffers, and returns clean JSON results. This prevents infinite blocking loops and protects system stability."*

#### `3:15 - 4:30` | Explaining One Guardrail & One Real Limitation (On Camera)
* **Screen Visual:** Open `system_prompt.md` in VS Code and highlight the **Human-in-the-Loop Gate** section.
* **Narration Script:**  
  > *"For safety, CodePulse operates under a strict Human-in-the-Loop guardrail: it will never run `git push` or mutate production databases without explicit user confirmation. Now, regarding limitations: currently, CodePulse executes test suites in local subshells. In a multi-tenant cloud environment, running tests locally limits scalability. Our v2 roadmap will move execution to isolated AWS EC2 Docker containers over SSH."*

#### `4:30 - 5:00` | Conclusion & Links
* **Screen Visual:** Return to browser showing `https://github.com/NivedhN160/AI-Fluency-Capstone`.
* **Narration Script:**  
  > *"Thank you for watching! All code, live MCP tools, and reproducible instructions are available on GitHub at NivedhN160/AI-Fluency-Capstone and live at ai-fluency-capstone.netlify.app."*

---

## 📝 Section 3: Portal Submission Format

```text
FL-09: Documentation and Demo Video Submission

1. Capstone GitHub Repository: https://github.com/NivedhN160/AI-Fluency-Capstone
2. Capstone README: https://github.com/NivedhN160/AI-Fluency-Capstone/blob/main/README.md
3. Live Web Showcase: https://ai-fluency-capstone.netlify.app
4. Demo Video Link (Unlisted YouTube): https://www.youtube.com/watch?v=rraHPF4ZgCw (or your uploaded video link)
```
