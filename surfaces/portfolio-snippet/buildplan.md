# Portfolio Build Plan — Windows XP Edition, Self-Updating
## Leave github part i will host on render and add a cronjob to ping eery 10min to keep the website away from spinning down
## The concept in one line

A portfolio that looks and feels like Windows XP (desktop icons, draggable windows, a Start menu, maybe a fake "My Computer"), where the **Projects folder auto-populates from your GitHub** — no manual editing every time you ship something. You push a new repo, it shows up. The system also picks **one "Featured Project"** automatically based on README quality/content, so your best work always surfaces without you deciding by hand.

This builds on the portfolio you already have (`nivedhn160.github.io`, Windows XP themed, currently on GitHub Pages) — we're upgrading it from static to self-updating, and giving you a path to Render if/when you want a live backend instead of a build-time pipeline.

---

## Part 1 — Decide the architecture (read this before building anything)

There are two fundamentally different ways to do "auto-updating," and picking the wrong one wastes weeks. Here they are, with a clear recommendation.

### Option A — Static, build-time generation (recommended)
A script runs on a schedule (via **GitHub Actions**, which is free and exactly built for this), fetches your repos + READMEs from the GitHub API, picks the featured one, writes a `projects.json` file, and the static XP-themed site reads that file. No server runs 24/7. No cold starts. No Render needed at all unless you want one later.

- **Cost:** $0, forever. GitHub Actions free tier gives you 2,000 minutes/month on public repos (you'll use maybe 1 minute per run).
- **Hosting:** GitHub Pages (free, no spin-down, no cold start) — keep what you already have.
- **Reliability:** extremely high. Nothing is "running" that can crash.

### Option B — Live backend, fetches on each page load
A small server (Node/Express, FastAPI, whatever) calls the GitHub API every time someone visits your site, picks the best project live, and renders it. This is the option that benefits from Render.

- **Cost:** $0 if you accept the free-tier tradeoff — but **Render's free web services spin down after 15 minutes of inactivity** and take 30-60 seconds to wake up on the next visit. That means the *first* visitor after a quiet period sees a slow/broken-looking site. Not a great first impression for a portfolio.
- **Mitigation:** ping your own Render service every ~10-14 minutes using a free external cron service (e.g. cron-job.org) to keep it warm — this works, but it's an extra moving part for something that doesn't need to be live in the first place.
- **When this is worth it:** if you want real-time features later (a contact form with a database, an admin panel, live visitor analytics) — not just for "show my latest projects."

### Recommendation
**Use Option A as the core mechanism.** It's simpler, free with zero caveats, and a portfolio doesn't need server-side logic per visit — it needs to be *correct as of your last push*, not *correct to the millisecond*. You can still deploy a **copy** to Render later as a live mirror/experiment (good talking point: "also deployed via Render with a Postgres cache" if you want extra infra credibility), but it shouldn't be the thing your site depends on to function.

---

## Part 2 — System architecture

```
┌─────────────────────┐
│   Your GitHub repos   │
│  (any repo you push) │
└──────────┬───────────┘
           │ GitHub REST API
           ▼
┌────────────────────────────┐
│  GitHub Actions workflow    │   ← runs daily, or on every push
│  (Node/Python script)       │
│                              │
│  1. List all your public    │
│     repos                   │
│  2. Fetch each README       │
│  3. Score each README        │
│  4. Pick the "Featured" one │
│  5. Write projects.json     │
└──────────┬───────────────────┘
           │ commits projects.json
           │ back into the repo
           ▼
┌────────────────────────────┐
│  Static portfolio site      │
│  (HTML/CSS/JS, XP theme)    │
│  reads projects.json at     │
│  load time via fetch()      │
└──────────┬───────────────────┘
           │
           ▼
┌────────────────────────────┐
│  GitHub Pages (or Render    │
│  static site, both free)    │
└────────────────────────────┘
```

---

## Part 3 — The "pick the best project" logic

This is the most interesting engineering problem in the whole build, and it's worth doing properly rather than something trivial like "most stars" (you don't have many stars yet, and star count rewards popularity, not quality).

### Scoring signals to pull from each README (all free, all from data you already have)

| Signal | How to extract it | Why it matters |
|---|---|---|
| README length (in words) | simple word count | very short READMEs are usually unfinished/placeholder |
| Presence of a description/intro paragraph | check first 200 words for sentence structure | signals the author explained *what* and *why* |
| Code blocks present | count of ` ``` ` fences | signals technical depth/usage docs |
| Has an architecture/diagram section | regex for "architecture", "diagram", mermaid blocks | signals more serious engineering documentation |
| Has install/usage instructions | regex for "install", "usage", "getting started" headers | signals it's actually usable, not just a dump |
| Has a live demo link | regex for URLs near "demo", "try it", "live" | signals it's deployed, not just code |
| Last commit recency | from GitHub API `pushed_at` | recently active projects feel more "current" |
| Repo language matches target stack | from GitHub API `language` field | lets you weight AI/Python/Zig projects higher if you want |
| Number of README sections (headers) | count of `##`/`###` | a well-structured README usually means a more thought-through project |

### A simple, transparent scoring formula
Don't overengineer this with ML — a weighted point system is more than enough and is fully explainable (good if you ever want to write about it):

```
score =
    (readme_word_count > 150 ? 10 : 0) +
    (has_intro_paragraph ? 10 : 0) +
    (code_block_count * 3, capped at 15) +
    (has_architecture_section ? 15 : 0) +
    (has_usage_section ? 10 : 0) +
    (has_live_demo_link ? 20 : 0) +
    (days_since_last_push < 30 ? 10 : 0) +
    (header_count * 2, capped at 10)
```

Whichever repo scores highest becomes "Featured" — displayed prominently (e.g. opened in a maximized "window" by default, or pinned to the top of the Projects folder icon grid).

### Nice upgrade later
Once this works, you could swap the manual scoring formula for an actual LLM call (free tier of Groq or Gemini) that reads each README and rates it 1-10 with a one-line justification — genuinely more accurate, and gives you a fun feature: each project window could show "Why this was featured: ___" as an XP-style tooltip/balloon notification. Keep this as a v2 enhancement, not a day-1 requirement — the manual scoring system above is zero-dependency and ships faster.

---

## Part 4 — Build order

### Phase 1: Data pipeline (the "auto-update" core) —
1. Write a script (Node.js or Python — Python is easier for README text processing) that:
   - Calls `GET https://api.github.com/users/NivedhN160/repos` to list all public repos
   - For each repo, calls `GET /repos/{owner}/{repo}/readme` to fetch README content (returned base64-encoded, decode it)
   - Runs the scoring formula above on each README
   - Outputs a `projects.json` file shaped like:
     ```json
     {
       "generated_at": "2026-06-24T12:00:00Z",
       "featured": "ZigNGPTv2.0",
       "projects": [
         {
           "name": "ZigNGPTv2.0",
           "description": "...",
           "url": "https://github.com/NivedhN160/ZigNGPTv2.0",
           "language": "Zig",
           "score": 78,
           "last_updated": "2026-06-20"
         }
       ]
     }
     ```
2. Test this script locally first — run it, inspect the JSON, sanity check the featured pick makes sense.
3. **Use a GitHub personal access token** (even for public repos, this avoids GitHub's strict unauthenticated rate limits — 60 requests/hour unauthenticated vs 5,000/hour authenticated). Store it as a GitHub Actions secret, never commit it.

### Phase 2: Automate it —
1. Add a GitHub Actions workflow file (`.github/workflows/update-projects.yml`) that:
   - Runs on a schedule (e.g. daily via `cron`) **and** on `push` to any repo if you want near-instant updates (this requires a small trick — see "Triggering across repos" below)
   - Runs your script from Phase 1
   - Commits the updated `projects.json` back to your portfolio repo automatically
2. **Triggering across repos** (the "new repo shows up automatically" part): GitHub Actions in one repo can't natively watch *all* your other repos for pushes. Two ways to solve this:
   - **Simple (recommended to start):** just run on a daily schedule. New repos/READMEs will show up within 24 hours — totally fine for a portfolio, nobody needs millisecond freshness.
   - **More real-time:** add a tiny `repository_dispatch` step to every other repo's own Actions workflow that pings your portfolio repo's Actions API whenever it pushes. This is more setup per-repo, so only do this once the daily version is working and you want the instant version as a polish pass.

### Phase 3: The Windows XP frontend — (the part you'll spend most time on)
This is the part most people would suggest doing first — don't. Build the data pipeline first so you have real JSON to render against, instead of guessing at a shape and refactoring later.

1. **Desktop shell**: background image (classic XP "Bliss" green hills, or your own twist on it), desktop icons (My Computer, Recycle Bin, a "Projects" folder, a "Resume.exe", "Contact.exe")
2. **Window manager**: draggable, resizable windows with the XP titlebar (minimize/maximize/close buttons), since this is the centerpiece interaction of the whole theme
3. **Start menu**: classic green Start button, menu items linking to sections (About, Projects, Contact, Resume)
4. **Projects folder**: double-clicking it opens a window styled like a Windows Explorer file browser, where each project is a "file/folder icon" — clicking one opens a project detail window (description, tech stack, links, pulled straight from `projects.json`)
5. **Featured project**: on desktop load, auto-open the featured project's window (like a "welcome" popup), or give it a special icon treatment (a little star badge, or place it first in the Explorer-style list)
6. **Fun XP details that cost little but add a lot of charm**: a fake BSOD easter egg, the XP startup sound on load (mutable), a clippy-style assistant balloon that says something sarcastic (tie this back to your ZigNGPT personality — very on-brand), right-click context menus on desktop icons

### Phase 4: Hosting — half a day
- **Primary:** GitHub Pages, same as your current setup — push to `main`, it's live. Free, zero spin-down, zero cold starts.
- **Optional Render mirror:** if you want it, deploy the same static site as a Render Static Site (not a web service — static sites on Render don't spin down the way web services do, and are free). This gives you a talking point about multi-platform deployment without taking on any of the cold-start risk from Option B above.

---

## Part 5 — Tech stack summary (all $0)

| Layer | Tool | Cost |
|---|---|---|
| Data fetching script | Python or Node.js | Free |
| Scheduler/automation | GitHub Actions | Free (public repo) |
| README → JSON storage | flat `projects.json` in repo | Free |
| Frontend | Vanilla HTML/CSS/JS, or React if you want to reuse skills from your other projects | Free |
| Hosting | GitHub Pages (primary) | Free |
| Optional mirror | Render Static Site | Free |
| GitHub API auth | Personal Access Token (read-only, public repo scope) | Free |

---

## Part 6 — What this demonstrates (for your "must show I'm hireable" goal)

- **API integration** (GitHub REST API, auth, rate limit handling)
- **Automation/CI-CD thinking** (GitHub Actions, scheduled jobs, generated artifacts committed back to source control)
- **Practical scoring/ranking system design** (the README scoring formula — explainable, testable, extensible to ML later)
- **Frontend craft** (a non-trivial UI metaphor — draggable windows, a desktop simulation — is meaningfully harder than a template portfolio, and visually memorable)
- **Infra awareness** (you'll be able to explain *why* you chose static generation over a live backend, including the Render cold-start tradeoff — that's a real systems-design conversation, not just "I deployed it")

---