# 🛡️ FL-12: Break Your Own Site — Checkpoint 2 Hardening Review

**Track:** General AI Fluency (Week 9)  
**Deliverable:** Adversarial Break-Testing Log, SEO/Speed Audit, and Triage Matrix (Checkpoint 2 Pass)  
**Live Portfolio URL:** [https://nivedh-portfolio.netlify.app](https://nivedh-portfolio.netlify.app)  
**Live Capstone URL:** [https://ai-fluency-capstone.netlify.app](https://ai-fluency-capstone.netlify.app)  

---

## 📌 Executive Summary

Checkpoint 2 (Hardening Review) evaluates the production stability of the personal engineering portfolio beyond the happy path. This report logs adversarial testing across empty inputs, garbage payloads, rapid double-clicks, cross-browser viewports, SEO findability tags, and PageSpeed metrics.

---

## 🧪 Section 1: Adversarial Break-Testing Log ("Where It Breaks")

| Edge Case Test | Attempted Action | Initial Behavior / Output | Hardening Fix Implemented | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **1. Empty & Whitespace Form Submission** | Clicked submit on contact form with zero text or whitespace. | Native browser default allowed whitespace. | Added HTML5 native `required`, `type="email"`, and `minlength="2"` / `minlength="5"` attributes. | **PASSED (Blocked)** |
| **2. XSS & Garbage Payload Ingestion** | Submitted `<script>alert('XSS')</script>` in Name & Message fields. | Unfiltered text sent in POST request body. | Verified Netlify Forms server-side HTML entity escaping (`&lt;script&gt;`). Payload sanitized in dashboard. | **PASSED (Sanitized)** |
| **3. Rapid Double Submission** | Double-clicked "Send Message" button rapidly (100ms interval). | Duplicate HTTP POST requests sent to server. | Implemented client-side submit handler: `btn.disabled = true; btn.innerText = 'Sending Message... ⏳'`. | **PASSED (Mitigated)** |
| **4. Broken Link Audit** | Crawled all 11 header, footer, CTA, and case study links. | 11 / 11 links resolved. | Verified active HTTPS endpoints to GitHub repos, LinkedIn, and Proof Statement. | **PASSED (100% 200 OK)** |
| **5. Multi-Device Layout Break Test** | Tested viewports at 375px (iPhone), 768px (iPad), and 1440px (Desktop). | Zero horizontal scrolling or layout wrapping glitches. | Enforced CSS grid auto-fit, fluid `max-width: 960px`, and 48px touch target button bounds. | **PASSED (Responsive)** |

---

## 🔍 Section 2: Findability, SEO Meta Tags & PageSpeed Audit

### 1. Open Graph & Twitter Card Meta Tags
Integrated structured metadata in the `<head>` of `index.html` to ensure high-fidelity social previews when sharing links on LinkedIn, Twitter, Slack, or Discord:

```html
<!-- Open Graph / Facebook Meta Tags -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://nivedh-portfolio.netlify.app/">
<meta property="og:title" content="Nivedh — Systems & Backend Engineering Portfolio">
<meta property="og:description" content="Building resilient software from bare-metal C kernels to Dockerized FastAPI backends, background job queues, and automated PDF report generators.">

<!-- Twitter Card Meta Tags -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://nivedh-portfolio.netlify.app/">
<meta name="twitter:title" content="Nivedh — Systems & Backend Engineering Portfolio">
<meta name="twitter:description" content="Building resilient software from bare-metal C kernels to Dockerized FastAPI backends, background job queues, and automated PDF report generators.">
```

### 2. PageSpeed & Lighthouse Metrics
Ran Google PageSpeed Insights & Chrome Lighthouse speed audit on `https://nivedh-portfolio.netlify.app`:

* **Overall Performance Score:** **100 / 100**
* **First Contentful Paint (FCP):** **0.4 seconds**
* **Largest Contentful Paint (LCP):** **0.6 seconds**
* **Total Blocking Time (TBT):** **0 ms**
* **Cumulative Layout Shift (CLS):** **0.000**

---

## 📋 Section 3: Triage Matrix & Checkpoint 2 Hardening Pass

### 🔧 Fix-Now Items (Resolved)
1. **Form Input Validation:** Enforced `required` and minimum text length constraints across all input fields.
2. **Double-Submit Prevention:** Disabled submit button immediately upon form click to block duplicate POST payloads.
3. **SEO & Social Share Previews:** Added Open Graph and Twitter Card tags.
4. **Touch Target Size & Contrast:** Verified 48px minimum touch heights and 7.2:1 contrast ratio exceeding WCAG AA standards.

### 💡 Known Limitations (Documented)
1. **JavaScript Requirement for Loading State:** Button disabling feedback requires client-side JavaScript. If a visitor disables JS, Netlify's server-side form handler still processes the POST request cleanly as a fallback.

---

## 🔄 Checkpoint 2 Pass Status
* [x] **Adversarial Audit Complete:** Tested empty submissions, XSS payloads, rapid double-clicks, and cross-browser viewports.
* [x] **SEO & Social Previews Added:** Verified title tags, meta descriptions, Open Graph, and Twitter Cards.
* [x] **PageSpeed Performance Verified:** 100/100 Lighthouse performance score with zero layout shift.
* [x] **Triage Matrix Complete:** Fix-now items resolved; known limitations explicitly named.
