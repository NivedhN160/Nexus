# Nexus Web: System Architecture

Nexus is an integrated personal AI operations platform integrating modules built during the FlyRank AI internship + flagship projects into a single, cohesive, self-hosted web product.

## Free-First, Local-Default Design
**Nexus is designed to be free by default.** It does not require paid API keys to operate.
- **Default LLM:** Local inference via ZigNGPT or NGPT logic (set by `LLM_PROVIDER=local`).
- **Cloud LLM (Optional):** Groq is available for higher-speed/larger models but is **off by default** (`NEXUS_CLOUD_LLM=0`).
- **Billing/Stripe:** Completely removed. Metering is used only for local soft-quotas, telemetry, and hard-budget agent enforcement.

## Enterprise-Grade Core Infrastructure
Despite being local-first, Nexus uses advanced patterns to ensure stability:
- **Budget Enforcer:** Hard limit token tracking that cleanly stops unbounded agent execution.
- **Agent Lifecycle Hooks:** An Event Bus natively tracking run states and tool usages for UI observability.
- **Guardrails:** AI input/output scrubbing and strict allow-lists for agent tools.
- **Isolated Sandbox:** A protected local Python subprocess runner with timeouts for agent-generated code.
- **Multi-Type Persistent Memory:** Structured PostgreSQL embeddings organized by FACTS, HISTORY, KNOWLEDGE, and INSTRUCTIONS.

## Core Architecture

```text
Browser (Dark Mission-Control UI)
    │
    ▼
Nexus API (FastAPI) + Worker + Postgres + Redis (Docker Compose)
    │
    ├─ Brain: Orchestrator (Local default, Groq optional)
    ├─ Search: DuckDuckGo (Free web scraping)
    ├─ Content / Leads / Social / Images / Match / Audit
    ├─ Metering: Local usage tracking (No Stripe) + Enforced Budget
    ├─ Guardrails & Hooks: Embedded inside the core API runtime
    └─ Labs: Terra-X, Mock Presence (Degrades gracefully without keys)

## Surfaced Modules (Green Paths)

The following modules are fully wired and functional within the Nexus Web UI:

| Surface | Description | Provider Repo |
|---------|-------------|---------------|
| **Agent Console** | Chat, tool execution, and local LLM interface with sandboxing, guardrails, and memory types. | N.E.O.S, ZigNGPT, syrin-harness |
| **Content Pipeline** | Draft posts, rank images, and schedule social media. | flyrank-internship, AI-Image |
| **Lead Stream** | Widget ingestion, rate limiting, and dashboard viewing. | Flyrank-Backend-Capstone |
| **Social Graph** | Campaign management and scheduled publishing. | Multi-Platform-Social |
| **Matchmaking** | Semantic search and ephemeral chat. | MAT-CHA.AI |
| **Dev Audit** | Multi-step persistent audit sessions (CodePulse) and frustration signals. | AI-Fluency, opensre |
| **Labs** | Terra-X climate simulation, Stock Analyzer, and experimental Presence Context. | Terra-X, Realtime-stock, RuView |

## What is NOT in Nexus Web?
To maintain a robust, production-ready core, certain experimental projects remain separated:
- **N-OS:** The separate desktop OS interface.
- **Billing / Stripe:** Nexus is a personal tool; it does not charge users.