# 🧠 Week 7 Assignment: Build an AI Decision Flow with React Flow + Inngest

**Track:** Backend AI Engineering Track (Week 7)  
**Author:** Nivedh  
**Main Internship Repository:** [https://github.com/NivedhN160/flyrank-internship](https://github.com/NivedhN160/flyrank-internship)  
**Project Folder:** `week 7/ai_decision_flow/`  

---

## 📌 Deliverables & Features Built

1. **Visual Flow Canvas (`React Flow`):**
   - Interactive canvas with custom decision nodes (`CustomDecisionNode.tsx`).
   - Distinct **YES path** (emerald green `#10B981`) and **NO path** (rose red `#EF4444`) edges.
   - Interactive toolbar: Add nodes, connect nodes, and edit node prompts in real time.
2. **Inngest Workflow Engine (`src/inngest/functions.ts` & `server.ts`):**
   - Each node maps to an Inngest step (`step.run()`).
   - LLM sends prompt + user input context and enforces strict `YES` or `NO` responses.
   - Dynamic graph traversal following matching decision path until terminal node.
3. **Developer Experience & Polish (Phase 4):**
   - **Visual Execution State:** Highlights active nodes and animates active glowing edges (`#F59E0B`).
   - **Execution History Panel:** Real-time log drawer showing step numbers, node prompts, timestamped AI decisions, and target transitions.
   - **JSON Import / Export:** Export custom workflow graphs to `.json` files and load existing presets.
   - **Resilient Fallback:** Automatic rule-based evaluator fallback if LLM API keys are unset.

---

## 💻 Setup & Run Instructions

```bash
cd "week 7/ai_decision_flow"

# 1. Install dependencies
npm install

# 2. Start Inngest Backend Server (Port 3001)
npm run server

# 3. Start React Flow Frontend (Port 5173)
npm run dev
```

---

## 📝 Portal Submission Text

```text
Week 7 Assignment Submission: Build an AI Decision Flow with React Flow + Inngest

1. GitHub Repository Deliverable: https://github.com/NivedhN160/flyrank-internship/tree/main/week%207/ai_decision_flow
2. Project README & Architecture: https://github.com/NivedhN160/flyrank-internship/blob/main/week%207/ai_decision_flow/README.md
3. Assignment Deliverable Summary: https://github.com/NivedhN160/flyrank-internship/blob/main/week%207/fl_ai_decision_flow_deliverable.md

Summary:
- Built visual AI workflow system using React Flow (@xyflow/react) with custom decision nodes and distinct YES (green) and NO (red) edges.
- Integrated Inngest step-functions (step.run()) executing LLM YES/NO decision logic and dynamic graph traversal.
- Added visual execution state, glowing active edge animations, timestamped execution log drawer, and JSON import/export functionality.
```
