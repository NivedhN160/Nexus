# Nexus Web

**Nexus** is an integrated personal AI operations platform. It unifies multiple real, production-tested AI and backend modules into a single, cohesive, self-hosted web product. 

This is not a mock or a demo—it is a functional monorepo powered by local AI, robust APIs, and disciplined backend operations (idempotency, rate limits, probes).

## Free-First & Local-Default
Nexus is built to be **100% free by default** for you and your users.
- **No Payment Provider:** Stripe has been completely removed. There is no billing wall.
- **No Required Paid APIs:** The agent brain defaults to local LLM infrastructure (`ZigNGPT` / `NGPT-llm-based`). 
- **Optional Cloud:** You can opt-in to using Groq for faster/larger inference by providing an API key and enabling `NEXUS_CLOUD_LLM=1`. Otherwise, the cloud remains entirely off.
- **Search:** Uses DuckDuckGo via web scraping patterns instead of paid search APIs.

## The Modules (Green Paths)
Nexus is composed of several "Green Paths" that are fully wired and functional in the dark mission-control UI:

1. **Agent Console (`N.E.O.S` / `ZigNGPT`)**: Chat and tool execution powered by local AI.
2. **Lead Stream (`Flyrank Leads`)**: Ingests portfolio widget submissions securely with honeypots, rate limiting, and geo-tracking.
3. **Content Pipeline & Social Graph (`Flyrank Content/Social`)**: Drafts posts, ranks images for mismatch guarding, and schedules multi-platform campaigns.
4. **Dev Audit (`AI-Fluency`)**: Analyzes frustration signals and generates CodePulse audit reports.
5. **Matchmaking (`MAT-CHA.AI`)**: Semantic search and ephemeral chat threading.
6. **Labs**: Experimental integrations like the Terra-X climate simulation and Real-time Stock Analyzer.

*(Note: Highly experimental OS-level interfaces like `N-OS` and standalone compiler projects are deliberately kept separate from this web core to ensure production stability.)*

## Getting Started

Nexus runs entirely via Docker Compose. There is only one path to boot the system.

1. Clone the repository.
2. Review the `.env.example` and create a `.env` file. (By default, no API keys are required).
3. Run the stack:
   ```bash
   docker compose up --build
   ```
4. Access the dark mission-control UI at `http://localhost:5173`.
5. The API is available at `http://localhost:8000` and Postgres/Redis are exposed on standard ports for local inspection.
