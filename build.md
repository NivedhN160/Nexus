# Nexus — Full System Spec (No Phases)

Build **everything below as one product**. Do not stage by “P1/P2”. Implement the complete personal AI operations platform.

---

## 1. Product definition

**Nexus** is a single-user personal AI operations platform.

One desktop/web application where the user talks to an agent that can:

- chat and use tools with visible tool cards  
- research the web and score buying signals  
- create content, match images, schedule social campaigns  
- capture leads via an embeddable widget  
- meter LLM/vision usage and enforce quotas  
- matchmake (semantic search, chat, mutual confirm)  
- run code audits and optional emotion/frustration signals  
- open the Terra-X climate lab  

**Not** a multi-tenant public SaaS. One operator (Nivedh). One API key is enough.

---

## 2. How the whole system must work

```
User
 └─ Nexus Shell (dark mission-control UI)
      ├─ Agent mode (default): chat + voice + tool cards
      ├─ Content mode: posts, images, social campaigns
      ├─ Leads mode: widgets, submissions, KPIs
      ├─ Match mode: search, threads, confirm
      ├─ Dev mode: affect indicator + CodePulse audit
      └─ Labs mode: launch Terra-X
           │
           ▼
      Brain (orchestrator)
           │ tool calls + domain API calls
           ▼
      Models | Tools | Domain services
           │
           ▼
      Postgres + Redis + background workers
```

**Global rules**

- Every tool/service call shows a **tool card**: name, args summary, result/error, latency_ms  
- Bottom **ops strip** always shows: last tool, latency, tokens used, quota bar  
- Errors and quota hits are **visible** (amber/red), never silent  
- Money is always **integer micro-cents** (no floats)  
- Publish and meter calls support **Idempotency-Key**  
- Public widget and signed webhooks verify input; never trust clients  

---

## 3. UI shell (must look and behave like this)

**Theme:** dark `#0B0F14` / `#111827`, glass panels, one teal accent, amber for warnings.

**Layout**

- Top: `NEXUS` | mode tabs | online indicator  
- Left: Agent, Content, Social (or under Content), Leads, Match, Dev, Labs  
- Center: main stage for active mode  
- Right: memory chips, active tools, usage snapshot  
- Bottom: ops strip (tool, latency, tokens, quota)

**Agent mode**

- Transcript: user / assistant / tool cards  
- Optional holographic orb (subtle)  
- Mic + waveform when voice on  
- Input box always available  

**Content mode**

- Post list with status: `draft | imaged | scheduled | published | failed`  
- Editor: title, markdown body, URL  
- Image panel: ranked candidates + reject reasons  
- Social panel: IG 1:1 and X 16:9 preview, captions, schedule datetime  
- Actions: Save, Rank images, Prepare campaign, Schedule  

**Leads mode**

- KPIs: submissions today, honeypot blocked, top geos  
- Table: time, widget id, geo, status  
- Widget config + copy-paste embed snippet  

**Match mode**

- Search query  
- Result cards with score/tags  
- Thread view + mutual confirm button/state  

**Dev mode**

- Optional camera status: calm | tense | frustrated  
- Button: Run CodePulse audit  
- Markdown report viewer  

**Labs mode**

- Tile: Open Terra-X (embed or external URL)

**Portfolio surface**

- Separate public site hosts embed:  
  `<script src="{API}/widget.js?id={widget_id}"></script>`  
- Widget UI: minimal glass form, same accent  

---

## 4. Brain (orchestrator) — full function set

Implement all of these:

| Function | Responsibility |
|----------|----------------|
| `handle_message(text, session_id)` | Full turn: plan → tools/services → final answer |
| `handle_voice_utterance(audio)` | STT → same as `handle_message` → optional TTS |
| `plan(intent, context)` | Decide tools/services and order |
| `call_tool(name, args)` | Execute adapter; return `{ok, result, error, latency_ms}` |
| `call_service(route, method, body, headers)` | HTTP to domain services with API key |
| `memory_read(session_id)` / `memory_write(...)` | Short-term session + optional long-term facts |
| `render_tool_card(...)` | Data for UI card |
| `estimate_or_record_usage(...)` | Hook into metering for billable calls |
| `model_complete(messages, tools)` | LLM with tool-calling; cloud primary, local fallback config |

**Tool registry (all registered and callable)**

- `web_agent.fetch` / `web_agent.extract`  
- `web_signals.scan`  
- `content.posts.*` (via service)  
- `images.rank`  
- `social.campaigns.*`  
- `leads.*` (admin; public submit is HTTP only)  
- `metering.record` / `metering.quota`  
- `match.search` / `match.chat` / `match.confirm`  
- `audit.run`  
- `affect.status` (optional continuous)  
- `climate.open`  

Agent must be able to chain: e.g. save post → rank images → create campaign → schedule.

---

## 5. Domain services — full APIs and behavior

Use one gateway (`apps/api`) or separate services behind it. All authenticated admin routes use `X-API-Key` except public widget submit and verified webhooks.

### 5.1 Content core

| Endpoint / fn | Behavior |
|---------------|----------|
| `POST /posts` | Create post `{title, body, url?}` → `draft` |
| `GET /posts` | List + filter by status |
| `GET /posts/{id}` | Detail |
| `PATCH /posts/{id}` | Update fields/status |
| `DELETE /posts/{id}` | Delete |

Statuses: `draft → imaged → scheduled → published` (and `failed`).

### 5.2 Images

| Endpoint / fn | Behavior |
|---------------|----------|
| `POST /images/index` | Index/batch image library (metadata + embeddings) |
| `POST /posts/{id}/rank-images` | Rank images for post text; return list with scores |
| Mismatch guard | Reject below similarity/confidence or subject mismatch; return **reason string** |
| Cost | Record vision/embedding cost via metering |

### 5.3 Social campaigns

| Endpoint / fn | Behavior |
|---------------|----------|
| `POST /campaigns` | From post_id: build IG + X variants (image dims + captions) |
| `POST /campaigns/{id}/schedule` | `{run_at}` → worker queue; idempotent |
| `GET /campaigns/{id}` | Status: queued | publishing | published | failed |
| Token storage | OAuth tokens **AES-256-GCM** at rest; decrypt only in memory |
| Publish | Adapter interface; **fake Instagram/X adapters allowed** but real interface shape required |
| 429 handling | Respect Retry-After backoff |
| Delivery webhook | `POST /webhooks/social-delivery` HMAC-SHA256 verify; reject invalid |

Worker must **crash-recover**: if process dies after external id assigned, do not double-post (idempotency + external_post_id check).

### 5.4 Leads / widgets

| Endpoint / fn | Behavior |
|---------------|----------|
| `POST /admin/widgets` | Create widget config |
| `GET /admin/widgets/{id}` | Config |
| `GET /widgets/{id}/config` | **Public** cached config for embed (CORS) |
| `GET /widget.js` | **Public** script loader |
| `POST /submissions` | **Public** lead submit: validate → size limit → rate limit → honeypot (silent drop) → geo fallback chain → store → optional email side effect (failure must not drop lead) |
| `GET /admin/submissions` | List |
| `GET /admin/stats` | KPIs |

### 5.5 Metering / billing

| Endpoint / fn | Behavior |
|---------------|----------|
| `POST /metering/events` | Record usage with `Idempotency-Key`; no double count |
| Pricing | Input / cached input / output / reasoning / per-call fees in **micro-cents** |
| `GET /metering/usage` | Aggregates for UI |
| Quota check | Before billable work; over quota → **429** or **402** |
| `POST /webhooks/stripe` | Signature verify; ignore replays; upgrade plan in test mode |

All LLM and vision calls from brain/services must create metering events.

### 5.6 Match

| Endpoint / fn | Behavior |
|---------------|----------|
| `POST /match/search` | Semantic search → ranked candidates |
| `POST /match/threads` | Start ephemeral thread |
| `POST /match/threads/{id}/messages` | Send message |
| `POST /match/threads/{id}/confirm` | Mutual confirm state machine |

### 5.7 Audit (CodePulse)

| Endpoint / fn | Behavior |
|---------------|----------|
| `POST /audit/run` | Target path/repo: check secret isolation, run tests if configured, inspect scraper politeness heuristics, write Markdown report |
| `GET /audit/reports/{id}` | Fetch report |

Tools: fs read, subshell test runner, http politeness inspector, report writer (MCP-style is fine).

### 5.8 Affect

| Endpoint / fn | Behavior |
|---------------|----------|
| `GET /affect/status` | Latest `{state: calm|tense|frustrated, score, ts}` from CV pipeline when enabled |
| Pipeline | Face mesh / emotion / blink / head pose → frustration score (can port Emotion-Aware logic) |

### 5.9 Web tools

| Tool | Behavior |
|------|----------|
| `web_agent` | Navigate/fetch/extract structured content from URLs |
| `web_signals` | Input companies → dual-path job signal extraction → LLM score 0–10 + rationale → ranked list |

### 5.10 Climate lab

| Tool | Behavior |
|------|----------|
| `climate.open` | Return URL or embed config for Terra-X; optional lat/lon/scenario params |

### 5.11 Models

| Backend | Behavior |
|---------|----------|
| Cloud hybrid | Primary completions + tool calling (Groq/API); optional web search style retrieval |
| Local Zig path | Config flag to route simple chat offline (integrate or subprocess to ZigNGPT build); stub OK only if interface is real and documented |

---

## 6. Data model (minimum entities)

- `User` / single API key  
- `Post`  
- `Image` + embeddings/metadata  
- `Campaign` + `CampaignPost` (platform, external_id, status)  
- `Widget`  
- `Submission`  
- `MeteringEvent` (idempotency_key unique)  
- `Quota` / `Plan`  
- `MatchProfile` (or external refs)  
- `MatchThread` / `MatchMessage` / `MatchConfirmation`  
- `AuditReport`  
- `MemoryItem`  
- `OAuthToken` (ciphertext only)  

**Postgres** for durable data.  
**Redis** for rate limits, idempotency keys, short caches.  
**Workers** for social schedule + any async geo/email.

---

## 7. Repo layout to implement

```text
nexus/
├── Architecture.md
├── README.md
├── docker-compose.yml          # api, worker, postgres, redis
├── apps/
│   ├── agent/                  # UI shell + brain client
│   ├── api/                    # gateway + route mount
│   └── worker/                 # scheduler, webhooks side effects
├── services/
│   ├── leads/
│   ├── metering/
│   ├── social/
│   ├── images/
│   └── match/
├── tools/
│   ├── web_agent/
│   ├── web_signals/
│   ├── audit_mcp/
│   ├── affect/
│   └── climate/
├── packages/
│   ├── shared/                 # auth, money, idempotency, hmac, errors
│   ├── llm-cloud-hybrid/
│   └── llm-local-zig/
└── surfaces/
    └── portfolio-snippet/
```

Port logic from existing public repos; do not require git submodules of whole capstones.

---

## 8. Shared library (`packages/shared`) — must implement

- API key auth middleware  
- `Idempotency-Key` store (Redis)  
- HMAC-SHA256 verify/sign  
- AES-256-GCM encrypt/decrypt helpers  
- Micro-cent pricing helpers  
- Standard error schema `{code, message, details?}`  
- Tool result schema `{ok, result, error, latency_ms}`  

---

## 9. End-to-end flows (all required)

**Research**  
User asks → brain → `web_signals` or `web_agent` → tool card → ranked answer → optional memory save.

**Content publish**  
Save post → rank images (guard reasons in UI) → create campaign → schedule → worker publishes idempotently → status updates → metering for vision/LLM.

**Lead capture**  
Visitor submits widget → public API pipeline → admin Leads table + KPIs.

**Billing**  
Any billable call → quota check → execute → meter event (idempotent) → strip updates; over quota blocked with 429/402.

**Match**  
Search → thread → messages → mutual confirm.

**Dev**  
Run audit → report view; optional affect status in Dev mode.

**Lab**  
Labs tile / agent tool → Terra-X open.

**Offline**  
Config routes chat to local model path when enabled.

---

## 10. docker-compose must provide

- `api` (gateway)  
- `worker`  
- `postgres`  
- `redis`  
- env files via `.env.example` (no secrets committed)  

Commands documented in README: up, migrate/seed, run agent, run tests.

---

## 11. Testing requirements

- Unit/integration tests for: idempotent metering, quota boundaries, honeypot, social idempotent publish, webhook sig reject, mismatch guard reject  
- At least one automated path test for: create post → rank → create campaign  
- Public submit validation / rate limit tests  

---

## 12. README must state

- What Nexus is  
- How to run full stack  
- That fake social adapters are intentional unless real OAuth configured  
- Link to Architecture.md  
- Module mapping to source GitHub projects  

---

## 13. About description (GitHub)

```
Nexus — personal AI operations platform: agent shell, content/social/leads, LLM metering, matchmaking, web tools, and audit — integrated system built from flagship and FlyRank modules.
```

Topics: `agentic-ai`, `fastapi`, `monorepo`, `python`, `redis`, `postgres`, `personal-ai`

---

## 14. Definition of done (complete product)

All of the following work in one running stack:

1. Agent chat with visible tool cards  
2. Web research or buying-signal scan from agent  
3. Full content path: post → images → campaign → schedule → status  
4. Lead widget submit → visible in Leads  
5. Metering + quota on billable calls + ops strip  
6. Match search + confirm  
7. Audit report generation  
8. Labs opens Terra-X  
9. docker-compose brings up api, worker, postgres, redis  
10. Shared auth, idempotency, HMAC, micro-cents used consistently  

---

Build **this entire system**. Do not split delivery into phases. Prioritize a working monolith gateway + worker + agent UI that implements every function above, with adapters (including fake social) behind clean interfaces so real providers can be swapped later.