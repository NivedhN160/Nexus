# Nexus

Nexus is a personal AI operations platform. It provides a single-user agent shell, content/social/leads management, LLM metering, matchmaking, web tools, and audit capabilities—an integrated system built from multiple flagship modules.

## How to Run Full Stack

Nexus uses a unified monorepo structure, deploying all services via `docker-compose`.

1. **Environment Variables**: Copy the example file and populate your keys.
   ```bash
   cp .env.example .env
   ```
2. **Start the Stack**:
   ```bash
   docker-compose up --build -d
   ```
   This will bring up the API gateway, background worker, PostgreSQL, and Redis.
3. **Database Migration and Seeding**:
   ```bash
   # Run migrations
   docker-compose exec api alembic upgrade head
   # Seed demo data if needed
   docker-compose exec api python scripts/seed.py
   ```
4. **Agent UI**:
   Navigate to the `apps/agent` directory, install dependencies, and run the development server (e.g., `npm install && npm run dev`).
5. **Run Tests**:
   ```bash
   docker-compose exec api pytest
   ```

## Important Notes
- **Fake Social Adapters**: By default, the social publishing features use fake adapters. This is intentional to allow testing without configuring real OAuth apps for X (Twitter) and Instagram. You can swap these out for real implementations later.

## Documentation
- Detailed architecture and design principles can be found in [Architecture.md](./Architecture.md).

## Module Map
Nexus integrates the following projects into its monorepo layout:
- `apps/agent` → [N.E.O.S](https://github.com/NivedhN160/N.E.O.S)
- `apps/api` (Content) → [flyrank-internship](https://github.com/NivedhN160/flyrank-internship)
- `services/leads` → [Flyrank-Backend-AI-Engineering-Capstone](https://github.com/NivedhN160/Flyrank-Backend-AI-Engineering-Capstone)
- `services/metering` → [LLM-Usage-Metering-Billing-Service-Flyrank-Capstone](https://github.com/NivedhN160/LLM-Usage-Metering-Billing-Service-Flyrank-Capstone)
- `services/social` → [Multi-Platform-Social-Campaign-Publisher-Flyrank-Capstone](https://github.com/NivedhN160/Multi-Platform-Social-Campaign-Publisher-Flyrank-Capstone)
- `services/images` → [AI-Image-Understanding-Content-Matching-Engine-Flyrank-Capstone](https://github.com/NivedhN160/AI-Image-Understanding-Content-Matching-Engine-Flyrank-Capstone)
- `services/match` → [MAT-CHA.AI](https://github.com/NivedhN160/MAT-CHA.AI)
- `tools/web_agent` → [Browser-Agent](https://github.com/NivedhN160/Browser-Agent)
- `tools/web_signals` → [Browser-Use-Hackathon](https://github.com/NivedhN160/Browser-Use-Hackathon)
- `tools/audit_mcp` → [AI-Fluency-Capstone](https://github.com/NivedhN160/AI-Fluency-Capstone)
- `tools/affect` → [Emotion-Aware-Code-Debugging-Assistant](https://github.com/NivedhN160/Emotion-Aware-Code-Debugging-Assistant)
- `tools/climate` → [Terra-X](https://github.com/NivedhN160/Terra-X)
- `packages/llm-cloud-hybrid` → [NGPT-llm-based](https://github.com/NivedhN160/NGPT-llm-based)
- `packages/llm-local-zig` → [ZigNGPTv2.0](https://github.com/NivedhN160/ZigNGPTv2.0)
- `surfaces/portfolio-snippet` → [Portfolio](https://github.com/NivedhN160/Portfolio)
