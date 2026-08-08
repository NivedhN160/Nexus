```markdown
# Nexus — Personal AI Operations Platform
## Product Look, Behavior & Architecture

**Status:** Planned post-internship system  
**Owner:** Nivedh (NivedhN160)  
**Principle:** One daily-driver platform. Strong public repos = modules. Labs/toys excluded.

---

## 0. How Nexus must look

Nexus is not a random dashboard farm. It should feel like **one mission-control product**: dark, dense, calm, with a clear “agent is the center” hierarchy.

### 0.1 Design language

| Token | Choice | Why |
|-------|--------|-----|
| **Theme** | Dark base (`#0B0F14` / `#111827`), soft glass panels | Matches N.E.O.S holographic + Terra-X mission-control DNA |
| **Accent** | Single primary (electric teal or violet) + amber for warnings | One brand color; amber = quota / frustration / errors |
| **Type** | UI: Inter or Geist; mono: JetBrains Mono for logs/tools | Readable ops UI + terminal credibility |
| **Radius / blur** | 12–16px cards, light backdrop-blur | Glassmorphism without clutter |
| **Motion** | Short (150–250ms), no gratuitous loops | Feels engineered, not “AI slop” |
| **Density** | Comfortable-dense | Power user; not empty marketing page |

### 0.2 Primary shell (desktop-first)

```text
┌──────────────────────────────────────────────────────────────────────────┐
│  NEXUS          [Agent] [Content] [Leads] [Match] [Labs]     ⚙  ● online │
├──────────────┬───────────────────────────────────────────────┬───────────┤
│              │                                               │           │
│  NAV         │              MAIN STAGE                       │  CONTEXT  │
│              │                                               │           │
│  • Agent     │   (changes by mode)                           │  Memory   │
│  • Content   │                                               │  Tools    │
│  • Social    │                                               │  Usage    │
│  • Leads     │                                               │  Status   │
│  • Match     │                                               │           │
│  • Dev       │                                               │           │
│  • Labs      │                                               │           │
│              │                                               │           │
├──────────────┴───────────────────────────────────────────────┴───────────┤
│  TOOL STRIP:  last tool · latency · tokens · quota ████░░  72%           │
└──────────────────────────────────────────────────────────────────────────┘
```

- **Top bar:** product name, mode tabs, connection state  
- **Left nav:** modules (only what is installed)  
- **Main stage:** active work  
- **Right context:** memory snippets, active tools, metering snapshot  
- **Bottom strip:** always-on ops truth (tokens, quota, last tool)

### 0.3 Mode-by-mode UI

#### Agent (default — from N.E.O.S)

- Center: conversation transcript (user / agent / tool cards)  
- Optional **3D / holographic orb or panel** (N.E.O.S heritage) — subtle, not blocking text  
- Mic button + waveform when VAD active  
- Tool calls render as **collapsible cards**: `tool_name`, args, result, latency  
- Right: short-term memory chips + pinned facts  

**Feel:** cockpit + chat, not ChatGPT clone.

#### Content

- List/detail of posts (title, status: draft → imaged → scheduled → published)  
- Editor: markdown body + URL  
- **Image panel:** ranked candidates from image engine; rejected matches show mismatch reason (red/amber)  
- **Social panel:** IG 1:1 and X 16:9 previews, captions, schedule time  
- Primary CTA: `Prepare campaign` → `Schedule`  

**Feel:** content ops console.

#### Leads

- KPI row: submissions today, blocked by honeypot, top geos  
- Table: time, source widget, geo, status  
- Snippet box: copy-paste `<script src="…/widget.js?id=…">` for Portfolio  

**Feel:** lightweight CRM, not Salesforce.

#### Match (MAT-CHA.AI)

- Search bar: vibe / skills query  
- Cards: semantic score, tags  
- Thread: ephemeral chat; mutual confirm as clear success state  

**Feel:** focused matchmaking, not social network.

#### Dev

- Optional camera indicator (Emotion-Aware): calm / tense / frustrated  
- Big button: `Run CodePulse audit`  
- Report viewer: markdown audit output (secrets, tests, politeness)  

**Feel:** IDE companion, not another social app.

#### Labs

- Launch tiles only: **Terra-X**, later others  
- Terra opens embedded or external: 3D Earth + scenario controls  

**Feel:** tool drawer, not core daily path.

### 0.4 Portfolio (public surface)

- Clean personal site (existing Portfolio)  
- One **Nexus lead widget** (corner or section) — glass, minimal fields, same accent color  
- No full Nexus UI exposed publicly in v1  

### 0.5 Visual references (internal)

| Borrow from | What to keep |
|-------------|----------------|
| N.E.O.S | Holographic/agent presence, voice-first chrome |
| Terra-X | Glass mission-control, map/lab seriousness |
| MAT-CHA.AI | Card match UI, clear confirm states |
| FlyRank capstones | Swagger-grade clarity in settings/logs; probe-level honesty in status |

### 0.6 Must / must-not (look & feel)

**Must**

- Dark theme default  
- Always show **quota / errors** honestly (amber/red)  
- Tool activity visible (no silent magic)  
- One accent color family  

**Must not**

- Rainbow gradients, stock “AI brain” hero art  
- Five unrelated dashboards with different design systems  
- Hiding failures behind generic “something went wrong”  

---

## 1. What Nexus is

Nexus is a **personal AI operations platform**: one agent surface that can research the web, draft and distribute content, match collaborators, meter AI cost, assist while coding, and open specialized tools (climate lab, infra patterns).

You are the only required tenant in v1. Multi-tenant SaaS is optional later.

---

## 2. System behavior (how it behaves)

| Mode | User action | System behavior |
|------|-------------|-----------------|
| **Agent** | Voice or text | Plans, calls tools, reads/writes memory, answers with tool cards |
| **Research** | Ask for company/job signals | Browser stack scrapes/scores → ranked list in chat + optional save |
| **Content** | Submit draft | Save post → rank images (mismatch guard) → build social variants → schedule |
| **Growth** | Visitor submits widget | Validate → rate limit → honeypot → geo → store → show on Leads |
| **Billing** | Any billable LLM/vision call | Idempotent meter → quota check → 429/402 when exceeded |
| **Match** | Search or chat | Semantic retrieve → ephemeral thread → mutual confirm |
| **Dev** | Code + optional camera | Frustration signal; on demand CodePulse audit report |
| **Lab** | Open Terra-X | Scenario lab for coordinates/variables |
| **Offline** | Prefer local | ZigNGPT / hybrid local path; metering stub or skip |

---

## 3. Repository → module map

### Included (core product)

| Module ID | GitHub repo | Role in Nexus |
|-----------|-------------|----------------|
| `brain` | [N.E.O.S](https://github.com/NivedhN160/N.E.O.S) | Orchestrator: voice, memory, tools, main UI shell |
| `llm-cloud-hybrid` | [NGPT-llm-based](https://github.com/NivedhN160/NGPT-llm-based) | Hybrid LLM + retrieval + DuckDuckGo + voice I/O |
| `llm-local-zig` | [ZigNGPTv2.0](https://github.com/NivedhN160/ZigNGPTv2.0) | Offline assistant path |
| `web-agent` | [Browser-Agent](https://github.com/NivedhN160/Browser-Agent) | Browser automation tool |
| `web-signals` | [Browser-Use-Hackathon](https://github.com/NivedhN160/Browser-Use-Hackathon) | Buying-signal scanner tool |
| `content-core` | [flyrank-internship](https://github.com/NivedhN160/flyrank-internship) | API spine: CRUD, Postgres, auth, queues, reports |
| `leads` | [Flyrank-Backend-AI-Engineering-Capstone](https://github.com/NivedhN160/Flyrank-Backend-AI-Engineering-Capstone) | Widgets, rate limit, honeypot, geo, dashboard API |
| `metering` | [LLM-Usage-Metering-Billing-Service-Flyrank-Capstone](https://github.com/NivedhN160/LLM-Usage-Metering-Billing-Service-Flyrank-Capstone) | Usage, quotas, micro-cents |
| `social` | [Multi-Platform-Social-Campaign-Publisher-Flyrank-Capstone](https://github.com/NivedhN160/Multi-Platform-Social-Campaign-Publisher-Flyrank-Capstone) | Campaigns, encrypted tokens, scheduler, signed webhooks |
| `images` | [AI-Image-Understanding-Content-Matching-Engine-Flyrank-Capstone](https://github.com/NivedhN160/AI-Image-Understanding-Content-Matching-Engine-Flyrank-Capstone) | Vision, embeddings, mismatch guard |
| `match` | [MAT-CHA.AI](https://github.com/NivedhN160/MAT-CHA.AI) | Matchmaking + ephemeral chat |
| `affect` | [Emotion-Aware-Code-Debugging-Assistant](https://github.com/NivedhN160/Emotion-Aware-Code-Debugging-Assistant) | Frustration / emotion signals |
| `audit` | [AI-Fluency-Capstone](https://github.com/NivedhN160/AI-Fluency-Capstone) | CodePulse MCP audits |
| `climate` | [Terra-X](https://github.com/NivedhN160/Terra-X) | Climate scenario lab tool |
| `surface` | [Portfolio](https://github.com/NivedhN160/Portfolio) | Public site + widget host |

### Infra patterns only

| Module ID | Repo | Use |
|-----------|------|-----|
| `infra-cicd` | [customer-accounts](https://github.com/NivedhN160/customer-accounts) | CI/CD and container patterns |
| `infra-agentic-aws` | [Hacknight-blr-elastic-aws](https://github.com/NivedhN160/Hacknight-blr-elastic-aws) | Bedrock/MCP/Elastic patterns if you scale |

### Excluded

Course labs, forks, toys (helicopter games, neon cube, token demos, etc.), **N-OS** / **Compiler-Construction** (separate flagships), superseded one-offs unless mined for ideas only.

---

## 4. Logical architecture

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ PRESENTATION                                                             │
│  Agent shell (N.E.O.S look) │ Content/Leads/Match views │ Portfolio     │
│  Labs: Terra-X                                                                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────────┐
│ ORCHESTRATION — brain                                                    │
│  Intent · tool router · memory · voice · tool-result cards in UI         │
└─────────────────────────────────────────────────────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ Model layer  │    │ Tool adapters    │    │ Domain services  │
│ NGPT hybrid  │    │ web-agent        │    │ content-core     │
│ ZigNGPT      │    │ web-signals      │    │ images · social  │
│ Groq / APIs  │    │ climate · affect │    │ leads · metering │
│              │    │ audit            │    │ match            │
└──────────────┘    └──────────────────┘    └──────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────────┐
│ DATA & JOBS                                                              │
│  Postgres · Redis · workers · Chroma/SQLite memory · encrypted OAuth     │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Runtime flows

### Content publish

```text
User → Agent/Content UI
  → content-core: save post
  → images: rank + mismatch guard (UI shows accept/reject reasons)
  → social: variants + schedule (previews in UI)
  → metering: vision/LLM usage
  → UI: success state + links
```

### Leads

```text
Visitor → Portfolio widget (Nexus styling)
  → leads API → Leads table + KPIs update
```

### Research / match / dev / offline

As in behavior table: agent invokes tools; UI shows tool cards; Dev page shows affect + audit report; offline path skips cloud metering.

---

## 6. Shared contracts

| Concern | Contract |
|---------|----------|
| Auth | `X-API-Key` / `tenant_id` (single tenant OK in v1) |
| Idempotency | `Idempotency-Key` |
| Webhooks | HMAC-SHA256 |
| Money | integer micro-cents |
| Jobs | durable queue + crash recovery |
| Tools | `name` + JSON args + result + latency for UI cards |

Join modules ⇒ move rate limit / idempotency to **Redis**.

---

## 7. Target monorepo layout

```text
Nexus/
├── ARCHITECTURE.md              ← this file
├── docs/
│   └── UI.md                    ← optional expand of §0
├── apps/
│   ├── agent/                   ← brain + shell look
│   ├── api/
│   └── worker/
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
│   └── climate/
├── packages/shared/
├── surfaces/portfolio-snippet/
└── docker-compose.yml
```

---

## 8. Phased delivery

| Phase | Outcome | UI visible |
|-------|---------|------------|
| **P0** | Internship packs done | — |
| **P1** | Agent + 1 tool | Agent shell + tool cards |
| **P2** | Content loop | Content mode + image/social panels |
| **P3** | Growth | Leads mode + Portfolio widget |
| **P4** | Metering | Bottom strip quota + settings |
| **P5** | Match | Match mode |
| **P6** | Dev | Dev mode |
| **P7** | Labs | Labs tile → Terra-X |

---

## 9. Non-goals (v1)

- Public multi-tenant SaaS  
- Real social OAuth until needed  
- Merging N-OS into Nexus  
- Labs/toys in the dependency graph  
- Inconsistent light themes per module  

---

## 10. Success criteria

- [ ] Looks like **one** product (shared dark shell, accent, typography)  
- [ ] Agent is the default home  
- [ ] Content loop works without opening old capstone repos  
- [ ] Widget works on Portfolio  
- [ ] Quota and tool failures are visible in the UI  
- [ ] This document stays updated  

---

*Public repo sources: https://github.com/NivedhN160 — finish internship first; build Nexus second.*
```