# 🧠 AI Decision Flow — React Flow + Inngest Engine

> A visual AI workflow system built for Week 7 of the FlyRank AI Internship. Each node represents an AI decision step returning strictly **YES** or **NO**. Workflow execution runs through **Inngest step-functions** while the frontend visualizes the flow using **React Flow**.

[![React Flow](https://img.shields.io/badge/React%20Flow-xyflow-blue.svg)](https://reactflow.dev/)
[![Inngest](https://img.shields.io/badge/Inngest-Step%20Functions-purple.svg)](https://www.inngest.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-emerald.svg)](https://openai.com/)

---

## 🏗️ Architecture & Execution Flow

```text
User Input Query ("Our database is down!")
    │
    ▼
React Flow Canvas Editor (Interactive Nodes & YES/NO Edges)
    │
    ▼
Inngest Step Function (POST /api/execute-flow)
    ├─► Step 1: Support Request Check? ──► LLM Evaluator ──► YES
    │     └─► Traverses YES Edge (Green) ──► Node 2
    ├─► Step 2: Urgent Outage Check? ──► LLM Evaluator ──► YES
    │     └─► Traverses YES Edge (Green) ──► Node 4
    └─► Step 3: L3 PagerDuty Escalation ──► Final Action Triggered
    │
    ▼
Real-time Execution Drawer & Glowing Edge Visualization
```

---

## ✨ Deliverable Features Across All 4 Phases

### Phase 1: Setup & Environment
* [x] Next.js / Vite React application with TypeScript.
* [x] React Flow (@xyflow/react), Inngest client, and OpenAI SDK integration.
* [x] Environment variable configuration (`.env` and `.env.example`).

### Phase 2: Visual Flow Editor & Graph Foundations
* [x] Interactive React Flow canvas with custom `CustomDecisionNode` component.
* [x] Add new decision nodes and connect nodes dynamically.
* [x] Distinct edge types and colors: **YES path** (Green, `#10B981`) and **NO path** (Red, `#EF4444`).
* [x] Node prompt editor modal allowing live prompt modification.

### Phase 3: Core Inngest Step Execution
* [x] Each decision node maps to an Inngest step (`step.run()`).
* [x] LLM evaluates node prompt + user input and returns strictly `YES` or `NO`.
* [x] Dynamic graph traversal based on decision outputs.

### Phase 4: Polish & DX Improvements (4 Built)
1. **Visual Execution State & Glowing Edges:** Highlights active/visited nodes and animates active edges in real-time.
2. **Real-time Execution Logs Panel:** Timestamped step-by-step history showing LLM outputs and decision logic.
3. **JSON Export & Import / Save & Load:** Export workflow graphs to `.json` files and import existing templates.
4. **Resilient Error Fallback:** Automatic rule-based evaluator fallback if LLM rate limits occur.

---

## 💻 Reproducible Setup & Run Steps

### 1. Install Dependencies
```bash
npm install
```

### 2. Start Inngest Backend Server (Port 3001)
```bash
npm run server
```
*Inngest Dev Server Endpoint available at `http://localhost:3001/api/inngest`.*

### 3. Start React Flow Frontend (Port 5173)
```bash
npm run dev
```
*Open `http://localhost:5173` in your browser to interact with the visual AI workflow system!*

---

## 📄 License

Built by **Nivedh** for the **FlyRank AI Internship — Backend AI Engineering Track (Week 7)**.
