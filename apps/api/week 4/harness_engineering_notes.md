# 📹 Video Summary & Notes: Build the Systems That Build Software w/ Mirza Asceric

**Track:** Backend AI Engineering  
**Video URL:** [https://www.youtube.com/watch?v=rraHPF4ZgCw](https://www.youtube.com/watch?v=rraHPF4ZgCw)  
**Duration:** 90 min  
**Deliverable Link:** `https://www.youtube.com/watch?v=rraHPF4ZgCw`  

---

## 💡 Executive Summary & Core Concepts

### 1. The Paradigm Shift (Before vs. Now)
* **Traditional Engineering:** Writing every line of syntax by hand, debugging mechanical errors, and spending hours on boilerplate.
* **Harness Engineering:** Designing the automated systems, rules, specifications, and quality gates ("the harness") that enable AI agents to write, test, and refactor code safely.

---

## 🏗️ The 8 Pillars of Harness Engineering

### 1. Context is Memory
* LLMs have stateless context windows that reset between conversations.
* **Solution:** Provide persistent, structured context (standing project instructions, architecture guidelines, `.env.example` templates, and explicit schema definitions) so agents never have to guess codebase details.

### 2. The Knowledge Layer
* A codebase needs clear "maps" for both human engineers and AI agents.
* A well-structured `README.md`, clear directory layout, and self-documenting code modules act as the primary interface for AI agents.

### 3. The Spec Layer
* Ambiguous prompts lead to messy implementations.
* Write detailed specifications that define explicit criteria for success ("Done Means: tests pass, HTTP status codes match spec, no untracked files").

### 4. The Loop
* Turning specifications into shipped code via automated, repeatable execution loops.

### 5. Trust, Gates & Circuit Breakers
* **Rule:** Never trust an LLM's claim that code works without empirical verification.
* Enforce automated test suites, linters, build checks, and circuit breakers (timeout limits) so an agent cannot claim success on a failing build.

### 6. The Codebase as the Interface
* Modular architecture (like the **Repository Pattern** we built in Week 3) decouples storage from business logic.
* Strong typing, clean function signatures, and interface abstractions drastically improve AI code generation quality.

### 7. Running Parallel Agents
* Managing multiple specialized agents across isolated tasks or subdirectories without git merge conflicts or state corruption.

### 8. What Stays Human
* System architecture design, security boundaries, business priority decisions, and critical code reviews remain 100% human responsibilities.

---

## 🌐 Submission Link

```text
https://www.youtube.com/watch?v=rraHPF4ZgCw
```
