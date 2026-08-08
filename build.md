# Nexus Build Requirements & API Spec

## Goal
Build the `Nexus` API that unites the separate capstone/portfolio backend systems (leads, content, social scheduling, metering, matchmaking, and affect/audit) into one clean, robust FastAPI application, powered by local LLMs (ZigNGPT/NGPT) by default.

## Principles
1. **Free by Default:** No paid APIs required. Local LLM models are preferred. Stripe/billing is completely excluded.
2. **Postgres & Redis:** State goes in Postgres, queues/rate-limits go in Redis.
3. **Idempotency:** Protect billable/heavy LLM actions and social posts with `Idempotency-Key` headers.
4. **Security:** Use `X-API-Key` on internal routes; properly verify webhook signatures from external systems.
5. **No Vaporware:** Only implement routes that map directly to functional capabilities imported from the capstone repos.

## UI Shell (Dark Mission-Control)
The frontend (`apps/agent`) provides a unified, dark mission-control interface with the following core modules:
- **Agent Console:** Local LLM chat and tool execution.
- **Content Pipeline:** Draft generation and AI mismatch checking.
- **Social Graph:** Campaign scheduling and publishing.
- **Lead Stream:** Widget ingestion viewing.
- **Matchmaking:** Search and ephemeral chat.
- **Dev Audit:** Telemetry, health, and CodePulse audit reports.
- **Labs:** Optional experimental features (Terra-X).

## Core Data Models
| Table | Purpose |
|-------|---------|
| `Lead` | Submissions from the portfolio widget. |
| `Post` | Blog/content drafts (Content Pipeline). |
| `Campaign` & `CampaignPost` | Scheduled social media fan-out (Social Graph). |
| `MeteringEvent` | Internal soft-quota tracking for LLM token usage. |
| `SystemEvent` | Audit trail and health logs (Dev Audit). |

## API Routes Overview

### 1. Agent Brain (`/brain`)
| Route | Action |
|-------|--------|
| `POST /brain/chat` | Receives chat messages, executes local LLM by default, runs tools. |

### 2. Leads (`/leads`)
| Route | Action |
|-------|--------|
| `POST /leads` | Public endpoint for widget. Rate limited (Redis). Honeypot check. |
| `GET /leads` | Protected endpoint to fetch lead stream for the UI. |

### 3. Content Pipeline (`/content` & `/images`)
| Route | Action |
|-------|--------|
| `POST /content` | Generate/save drafts. |
| `POST /images/rank` | AI ranking to prevent image-content mismatch. |

### 4. Social Graph (`/social`)
| Route | Action |
|-------|--------|
| `POST /social` | Create campaign variants for IG/X from a post. |
| `POST /social/{id}/schedule` | Schedule a campaign to run. |
| `POST /social/webhooks/social-delivery` | Receive delivery confirmations (signature verified). |

### 5. Audit & Metering (`/audit` & `/metering`)
| Route | Action |
|-------|--------|
| `GET /audit/logs` | Fetch system health logs. |
| `GET /metering/usage` | Fetch local LLM usage against soft quotas. |

All routes except webhooks and `POST /leads` require the `X-API-Key` header matching the `.env` configuration.