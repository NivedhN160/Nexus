# 🤖 FL-05: Agent Concepts and MCP Basics Explainer

**Track:** General AI Fluency (Week 4)  
**Deliverable:** 600–900 Word Technical Explainer, MCP Primitives Analysis, and FL-04 Upgrade Roadmap  

---

## 🎯 1. Workflows vs. Agents: The Core Architectural Distinction

In modern AI engineering, the word "agent" is frequently overused. Anthropic's landmark essay *Building Effective Agents* establishes a clear architectural line between **Workflows** and **Agents**:

* **Workflows** are systems where Large Language Models (LLMs) and tools are orchestrated through **predefined, programmatic code paths**. The developer hardcodes the sequence of execution (e.g., Step A → Step B → Step C), and the model operates strictly within these boundaries.
* **Agents**, by contrast, are systems where the LLM **dynamically directs its own control flow**. Given a high-level goal, an agent formulates its own plan, chooses which tools to invoke, evaluates intermediate outputs from the environment, recovers from runtime errors, and decides when the task is complete.

### Classification of the FL-04 Pipeline
The automation pipeline built in **FL-04 (Ship an Automation Workflow v2)** is strictly a **Workflow (Prompt-Chaining & Sequential Processing)**, not an Agent. 

In FL-04, the sequence of execution was hardcoded:
1. *Step 1: Gather & Extraction* →
2. *Step 2: Architecture Synthesis* →
3. *Step 3: Draft Case Study & Code Review* →
4. *Step 4: Format & Verification*.

The AI model did not choose which step to execute next or dynamically alter its plan based on external environment feedback. It predictably followed a fixed assembly line designed by the engineer.

---

## 🔌 2. What is Model Context Protocol (MCP)?

The **Model Context Protocol (MCP)** is an open-source standard created by Anthropic that acts as a **standardized "USB-C port" for AI applications**. Before MCP, connecting an AI model to an external database, terminal, or API required custom, proprietary integration code for every client. MCP unifies these connections into a single open protocol.

MCP relies on three core primitives:

1. **Tools:** Executable functions exposed by an MCP server that allow the model to take actions in the real world (e.g., executing terminal commands, creating database tables, running code tests, or sending HTTP requests).
2. **Resources:** Read-only data sources or contextual files provided to the model (e.g., local codebase files, API documentation, database schemas, or live system logs).
3. **Prompts:** Pre-configured prompt templates and reusable instruction sets exposed by the server to guide how tasks are initiated.

---

## 🛠️ 3. Evidence of Working MCP / Connector Setup

To demonstrate MCP capabilities in practice, three distinct tasks were executed using tool integration that plain text chat alone could not perform:

### Task 1: Direct File System Inspection & Directory Traversal
* **Tool Used:** `list_dir` / `run_command`
* **What Happened:** The model directly queried the Windows NTFS file system at `E:\Flyrank internship\week 4\`, inspected directory tree structures, and verified virtual environment paths without requiring manual copy-pasting.
```json
{
  "tool": "run_command",
  "command": "powershell -Command \"Get-ChildItem 'E:\\Flyrank internship'\"",
  "output": "Directory: E:\\Flyrank internship\nweek 1, week 2, week 3, week 4"
}
```

### Task 2: Automated Local Test Suite Execution
* **Tool Used:** `run_command`
* **What Happened:** The model executed `python scratch/test_w4_endpoints.py` in an isolated subshell, invoked local FastAPI endpoints, and parsed raw HTTP response headers (`HTTP/1.1 200 OK`, `HTTP/1.1 401 Unauthorized`).
```json
{
  "tool": "run_command",
  "command": ".\\venv\\Scripts\\python test_w4_endpoints.py",
  "output": "=== 3. GET /protected/profile (No Token - 401) ===\nHTTP 401: {\"error\":\"Access token required\"}"
}
```

### Task 3: Local File Creation & Persistent Disk Mutation
* **Tool Used:** `write_to_file`
* **What Happened:** The model wrote `main.py`, `.env.example`, and `requirements.txt` directly to disk, creating persistent project files that survive server restarts.
```json
{
  "tool": "write_to_file",
  "target": "E:\\Flyrank internship\\week 4\\main.py",
  "status": "Created file file:///E:/Flyrank%20internship/week%204/main.py"
}
```

---

## 🚀 4. Concrete Upgrade: Turning FL-04 into a True Autonomous Agent

To upgrade the FL-04 pipeline from a static **Workflow** into a fully autonomous **Agent**, the following four architectural enhancements are required:

1. **Dynamic Tool Use via MCP:** Instead of manually pasting code files into prompts, equip the system with MCP tools (`read_file`, `git_commit`, `run_pytest`, `http_request`).
2. **Environmental Feedback Loop:** When generating a case study, the agent will automatically execute `pytest` or `curl -i` against the API server. If a test fails, the agent reads the error stack trace, modifies the code, and re-runs the test autonomously.
3. **Autonomous Step Planning:** Rather than following a rigid 4-step sequence, the agent inspects the repository, identifies missing tests or undocumented endpoints, and formulates its own execution plan.
4. **Circuit Breakers & Stopping Conditions:** Introduce safety guardrails, such as a `MAX_ITERATIONS = 5` circuit breaker and automated linting gates, to prevent runaway loops or infinite retries.

---

## 🔄 Pass / Revise Checklist
* [x] **Explainer Length & Clarity:** 600–900 words written in original, technical natural language.
* [x] **Workflow vs Agent Applied:** Accurately classified FL-04 as a prompt-chaining workflow.
* [x] **MCP Primitives Defined:** Detailed Tools, Resources, and Prompts.
* [x] **Demonstrable MCP Tool Calls:** Documented 3 filesystem, execution, and disk mutation tasks with tool log outputs.
* [x] **Concrete Agent Upgrade Roadmap:** Named feedback loops, dynamic tool selection, and circuit breakers.
