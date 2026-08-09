# 🚀 Ship the Ugly One: Live Portfolio Release

**Track:** General AI Fluency (Week 5)  
**Deliverable:** Live Site URL, Real Reviewer Feedback, Code Explanation, and "Still Ugly" List  

---

## 🌐 1. Live Public URL

* **Public Portfolio URL:** [https://nivedh-portfolio.netlify.app](https://nivedh-portfolio.netlify.app)
* **GitHub Repository:** [https://github.com/NivedhN160/flyrank-internship](https://github.com/NivedhN160/flyrank-internship)
* **Status:** 100% Live, deployed on Netlify, tested across desktop and mobile devices.

---

## 📊 2. Real Work & Case Studies Included (Zero Placeholders)

The live site showcases 5 verified, end-to-end engineering case studies:
1. **Week 5 (BE-04): The Polite Web Scraper & RAG Corpus** — BeautifulSoup HTML extraction, `robots.txt` compliance, 1.5s rate-limiting, and Pydantic JSON/CSV export.
2. **Week 4 (BE-03): Auth Login & Bearer JWT Protect** — Supabase Auth Identity Provider (IdP), FastAPI `HTTPBearer` dependencies, and 401 token verification.
3. **Week 3 (BE-02): Postgres in Docker & Repository Pattern** — Data layer abstraction via `TaskRepository` and Docker Compose multi-container orchestration.
4. **Week 2 (BE-01): FastAPI Task CRUD REST API** — 9 REST endpoints with HTTP status code enforcement (201, 204, 400, 404).
5. **Week 1 (Systems): Bare-Metal Systems Focus & Proof Statement** — Custom C/Assembly OS kernel background and low-level engineering roadmap.

---

## 🗣️ 3. Real Person's Reaction & Feedback

Shared the live link with a senior software engineer / tech mentor.

* **What They Saw:** A crisp, minimalist engineering portfolio featuring a clear one-line claim (*"I build resilient, production-ready software from bare-metal C kernels to Dockerized FastAPI backends..."*) and 5 structured case studies matching the Slate identity kit (`#F8FAFC`, `#0F172A`, `#3B82F6`).
* **What Confused Them:** Asked why clicking "Read Case & Code Spec" redirected to GitHub markdown files instead of opening custom subpages on the same domain.
* **Did the Work Land?** **Yes.** The reviewer noted: *"Seeing real code repositories, explicit architectural decisions (Repository Pattern, Docker Compose, Supabase Auth), and raw `curl -i` status logs immediately sets this apart from typical student resume portfolios."*

---

## 💻 4. Code Explanation: How the Site is Built (No Mystery Code)

The portfolio is built using pure, clean **Semantic HTML5** and **Vanilla CSS3**:

1. **HTML5 Semantic Skeleton:** Built using `<header>` (sticky navigation), `<main>` (container wrapper), `<section>` (hero and case study grid), and `<footer>` (copyright and identity metadata).
2. **CSS Design Tokens (`:root`):** Color palette and typography tokens are declared as CSS variables (`--bg-color: #F8FAFC; --accent-color: #3B82F6; --font-heading: 'Plus Jakarta Sans'`).
3. **Responsive Grid Layout:** The case study grid uses `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));`, allowing cards to automatically reflow from 3 columns on desktop to 1 column on mobile screens without media query bloat.
4. **SVG Monogram Rendering:** The brand logo is an inline vector `<svg viewBox="0 0 64 64">` with a dark background badge and `#3B82F6` blue accent typography path.

---

## 📋 5. Honest "Still Ugly" List

The following elements are currently rough and scheduled for future polish:
1. **Direct GitHub Redirects:** Case study links open raw GitHub `README.md` files rather than styled subpages on the portfolio domain.
2. **No Dark Mode Toggle:** The site only supports the light Slate palette (`#F8FAFC`); needs an auto/manual dark theme toggle for night viewing.
3. **Static Screenshots vs. Live Sandboxes:** Case studies display text descriptions and code snippets rather than live, interactive REST API playgrounds.
4. **Minimal Micro-Animations:** Lacks subtle hover transitions or scroll-triggered fade-ins on card elements.

---

## 🔄 Pass / Revise Checklist
* [x] **Live Public URL:** Deployed and reachable on Netlify (`https://nivedh-portfolio.netlify.app`).
* [x] **Real Work Included:** All 5 weeks of real case studies embedded (no placeholders).
* [x] **Real Person's Reaction Captured:** Detailed mentor feedback recorded.
* [x] **Code Explained:** Full breakdown of HTML semantic structure, CSS grid, and SVG design tokens.
* [x] **Honest "Still Ugly" List:** Documented 4 specific areas for future refinement.
