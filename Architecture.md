# Nexus Web: System Architecture

Nexus is an integrated personal AI operations platform. It combines multiple modular tools and capstones into a single, cohesive, self-hosted web product.

## Free-First, Local-Default Design
**Nexus is designed to be free by default.** It does not require paid API keys to operate.
- **Default LLM:** Local inference via ZigNGPT or NGPT logic (set by `LLM_PROVIDER=local`).
- **Cloud LLM (Optional):** Groq is available for higher-speed/larger models but is **off by default** (`NEXUS_CLOUD_LLM=0`).
- **Billing/Stripe:** Completely removed. Metering is used only for local soft-quotas and telemetry.

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
    ├─ Metering: Local usage tracking (No Stripe)
    └─ Labs: Terra-X (Degrades gracefully without paid keys)
```

## Surfaced Modules (Green Paths)

The following modules are fully wired and functional within the Nexus Web UI:

| Surface | Description | Provider Repo |
|---------|-------------|---------------|
| **Agent Console** | Chat, tool execution, and local LLM interface. | N.E.O.S, ZigNGPT |
| **Content Pipeline** | Draft posts, rank images, and schedule social media. | flyrank-internship, AI-Image |
| **Lead Stream** | Widget ingestion, rate limiting, and dashboard viewing. | Flyrank-Backend-Capstone |
| **Social Graph** | Campaign management and scheduled publishing. | Multi-Platform-Social |
| **Matchmaking** | Semantic search and ephemeral chat. | MAT-CHA.AI |
| **Dev Audit** | CodePulse audit reporting and frustration signals. | AI-Fluency |
| **Labs** | Terra-X climate simulation and Stock Analyzer. | Terra-X, Realtime-stock |

## What is NOT in Nexus Web?
To maintain a robust, production-ready core, certain experimental projects remain separated:
- **N-OS:** The separate desktop OS interface.
- **Labs that require paid APIs:** Bedrock Civic Twin, heavy weather API demos (unless keys provided).
- **Billing / Stripe:** Nexus is a personal tool; it does not charge users.