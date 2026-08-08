# 🎨 FL-10: Survive the Crit (Design Review & Checkpoint 1 Pass)

**Track:** General AI Fluency (Week 7)  
**Deliverable:** Design Review Feedback, Proof Statement Comparison, Sorted Must-Fix List & Live Evidence  
**Live Site URL:** [https://nivedh-portfolio.netlify.app](https://nivedh-portfolio.netlify.app)  
**Proof Statement Reference:** [Week 1 Proof Statement](https://github.com/NivedhN160/flyrank-internship/blob/main/week%201/Proof_Statement.md)  

---

## 🗣️ 1. Mandatory 10-Second Test & Believability Answers

Submitted the live portfolio alongside the **Week 1 Proof Statement** to a senior tech mentor for structured review.

### Question 1: In ten seconds, what do I do?
> **Reviewer Answer:** *"You're a computer science / backend software engineer who builds low-level systems (C kernels) and production REST APIs, background job workers, and AI data scrapers."*  
> **Verdict:** **PASS.** The hero header claim (*"Nivedh — Systems & Backend Engineer"*) landed instantly within 10 seconds.

### Question 2: Would you believe I am good at it?
> **Reviewer Answer:** *"Yes. The code repositories, explicit architectural decisions (Repository Pattern, Docker Compose, HTTP 202 async background queue, ReportLab PDF rendering), and raw terminal logs make it very believable. It doesn't look like a generic template."*  
> **Verdict:** **PASS.** Proof statement backed up by real code artifacts.

---

## 📋 2. Honest Feedback Sorting: Must-Fix vs. Nice-to-Have

### 🔴 Must-Fix Items (Addressed Immediately on Live Site)
1. **Visual Technology Badges:** Card descriptions were purely text paragraphs. The reviewer suggested adding visual technology tags so visitors scanning the page can instantly see the stack (`FastAPI`, `Docker`, `Postgres`, `Supabase Auth`, `ReportLab`).
2. **Hero CTA Action Clarity:** Both hero buttons were equally weighted. The reviewer recommended sharpening the primary button label to *"Inspect Code & Artifacts on GitHub ➔"* to reinforce the single most important action.
3. **Footer Attribution:** Make track accreditation explicit in the footer (`FlyRank AI Internship — General AI Fluency & Backend AI Engineering`).

### 🟡 Nice-to-Have Items (Saved for Future Polish)
1. Interactive OpenAPI Swagger UI playground embedded directly in an `<iframe>` on the portfolio page.
2. Toggleable dark mode theme switcher for low-light viewing.
3. Micro-animations for card entry hover effects.

---

## 🛠️ 3. Evidence of Must-Fixes Addressed on Live Site

The following code updates were implemented in `index.html` and deployed live to [https://nivedh-portfolio.netlify.app](https://nivedh-portfolio.netlify.app):

### 1. Added Technology Stack Pills to Case Study Cards
```html
<div class="case-header">
  <span class="case-tag">Week 7 · BE-07</span>
  <span class="tech-pill">ReportLab / FastAPI</span>
</div>
```

### 2. Sharpened Primary Hero CTA Action
```html
<a href="https://github.com/NivedhN160/flyrank-internship" target="_blank" rel="noopener noreferrer" class="btn-primary">
  Inspect Code & Artifacts on GitHub ➔
</a>
```

### 3. Explicit Track Footer Attribution
```html
<p>© 2026 Nivedh. FlyRank AI Internship — General AI Fluency & Backend AI Engineering</p>
```

---

## 🔄 Pass / Revise Checklist
* [x] **Proof Statement Submitted:** Portfolio evaluated against Week 1 Proof Statement.
* [x] **10-Second Test Passed:** Reviewer identified exact role within 10 seconds.
* [x] **Believability Test Passed:** Reviewer confirmed real code repositories establish credibility.
* [x] **Feedback Sorted:** Honestly categorized into Must-Fix vs. Nice-to-Have.
* [x] **Must-Fixes Implemented Live:** Tech stack pills, CTA hierarchy, and footer attribution updated on live Netlify site.
