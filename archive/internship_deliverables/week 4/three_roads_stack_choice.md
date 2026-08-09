# 🛣️ Three Roads: Choose Your Stack with AI

**Track:** General AI Fluency (Week 4)  
**Deliverable:** Stack Evaluation, Pressure-Test Analysis, and Final Rationale  

---

## 🎯 1. The Four Core Constraints

1. **Cost Constraint:** 100% Free hosting, domain subdomains, and build tools.
2. **Honest Skill Level:** B.Tech Computer Science student comfortable with C, Assembly, Python (FastAPI), Docker, SQL, and core web fundamentals (HTML/CSS/JS).
3. **Portfolio Purpose & Content Map:** Showcasing backend architecture, low-level systems projects (custom OS, Zig LLM orchestrator), REST API case studies, and identity branding.
4. **Display Requirements:** High-contrast code blocks, terminal `curl -i` log snippets, interactive Swagger UI links, SVG visual monograms, and 3-beat case study narratives.

---

## 🏗️ 2. Three Stack Options Evaluated (Simplest to Most Powerful)

### Option 1 (Simplest): No-Code Builder (Framer / Webflow Free Tier)
* **How to Build:** Drag-and-drop visual interface components.
* **Hosting:** Framer/Webflow free subdomain (`.framer.media`).
* **Backend Required:** No.
* **Real Trade-Off:** Free tier includes unremovable platform banners/watermarks, hides underlying source code from Git, and limits custom syntax highlighting for C/Python code snippets. Feels like a designer's marketing site rather than an engineer's portfolio.

---

### Option 2 (Chosen Front-Runner): Semantic HTML5 + Vanilla CSS3 + Netlify / GitHub Pages
* **How to Build:** Handwritten semantic HTML5 structure, custom CSS design system (`Plus Jakarta Sans` + `Inter`, `#F8FAFC` Slate palette), deployed via continuous Git integration.
* **Hosting:** **Netlify** (Free tier with automatic GitHub continuous deployment).
* **Backend Required:** **Not yet** for the portfolio site itself (it is static presentation), while linking out to backend REST APIs (FastAPI + Postgres in Docker).
* **Real Trade-Off:** Adding new case studies requires updating HTML markup manually, but delivers 100% control, zero framework build errors, instant page loads, and zero vendor lock-in.

---

### Option 3 (Most Powerful): Full-Stack Next.js 14 + React + Tailwind CSS + Vercel
* **How to Build:** Component-based React framework with Server-Side Rendering (SSR) and Tailwind CSS utility classes.
* **Hosting:** Vercel (Free tier).
* **Backend Required:** Optional (Next.js API routes).
* **Real Trade-Off:** Massive bundle size, complex `node_modules` dependency management, potential framework breaking changes, and high setup friction for displaying static case studies.

---

## 🧪 3. Pressure-Testing the Options

| Pressure-Test Question | Option 1 (No-Code) | Option 2 (HTML5/CSS3 + Netlify) | Option 3 (Next.js + Vercel) |
| :--- | :--- | :--- | :--- |
| **What breaks if I pick it?** | Cannot version control source code in GitHub; free banners ruin technical credibility. | Nothing breaks. Static files serve reliably 100% of the time. | React hydration errors, npm dependency conflicts, and long build times. |
| **What do I maintain?** | Locked into Framer GUI interface. | Simple HTML/CSS files committed directly to Git. | Heavy `package.json`, framework upgrades, and React state. |
| **Can I finish in 2 weeks?** | Yes, but lacks technical polish. | **Yes, finished and deployed in 1 day.** | Risks spending 80% of time debugging React setup instead of writing case studies. |
| **Does it show my work well?** | Poorly for raw code snippets. | **Excellently. Displays raw code, logs, and SVGs cleanly.** | Well, but with unnecessary framework overhead. |

---

## 📝 4. Final Rationale (In My Own Words)

### Why I Chose Option 2 (Semantic HTML5 + Vanilla CSS3 + Netlify):
> "I chose a pure Semantic HTML5 and Vanilla CSS stack hosted on Netlify because it perfectly matches who I am as a systems and backend engineer. As someone building C kernels and Dockerized FastAPI backends, adding a heavy React/Next.js framework to display static text and code snippets creates unnecessary bloat and maintenance risk.
>
> Option 2 gives me 100% control over my code, zero build-step vulnerabilities, lightning-fast performance, and instant automatic deployments from GitHub to Netlify. I don't need a dynamic backend for my portfolio frontend *yet*—my backend expertise is proven through my case study links, Docker Compose repositories, and Swagger UI specs. I can easily maintain this stack forever without worrying about broken npm packages."

### Why I Rejected the Alternatives:
* **Rejected Option 1 (No-Code):** Watermarks and drag-and-drop GUIs obscure real code craftsmanship. A computer science student's portfolio should be built with actual code version-controlled in Git.
* **Rejected Option 3 (Next.js):** Over-engineering a static case study portfolio with a 200MB `node_modules` folder wastes build-week time on framework configuration instead of refining case study narratives and code proof.

---

## 🔄 Pass / Revise Checklist
* [x] **Three Genuine Options Evaluated:** Evaluated Framer (Simplest), HTML5/Netlify (Chosen), and Next.js/Vercel (Most Powerful).
* [x] **Matched Real Needs & Free:** 100% free hosting on Netlify with custom Identity Kit styling.
* [x] **Rationale in Own Words:** Clear, personal explanation addressing maintainability and proof display.
* [x] **Honest Backend Answer:** Correctly identified that the frontend portfolio needs no dynamic backend yet, while linking to real backend code.
