# 🚩 FL-13: Plant Your Flag — Domain, Analytics & Graduate Badge

**Track:** General AI Fluency (Week 9 Final Launch)  
**Author:** Nivedh (Computer Science Student & Systems / Backend Engineer)  
**Live Custom Portfolio Domain:** [https://nivedh-portfolio.netlify.app](https://nivedh-portfolio.netlify.app)  
**FlyRank Subdomain Target:** `nivedh.flyrank.ai`  
**FlyRank Verification Link:** [https://flyrank.ai/verify/nivedh](https://flyrank.ai/verify/nivedh)  
**GitHub Repository:** [https://github.com/NivedhN160/flyrank-internship](https://github.com/NivedhN160/flyrank-internship)  

---

## 📌 Executive Summary

This deliverable marks the final launch milestone for the **General AI Fluency** track. The personal engineering portfolio is fully deployed live over HTTPS with custom domain / subdomain resolution, free privacy-friendly web analytics, launch hygiene (favicon, social share previews, PageSpeed 100/100 score), and the official **FlyRank Graduate Verification Badge** installed in the footer.

---

## 🌐 Section 1: Live Domain & HTTPS SSL Certificate Status

* **Live Portfolio URL:** [https://nivedh-portfolio.netlify.app](https://nivedh-portfolio.netlify.app)
* **HTTPS Security:** Fully encrypted via Let's Encrypt TLS/SSL automated certificate.
* **FlyRank Subdomain DNS Configuration:**
  ```text
  Host: nivedh.flyrank.ai
  Type: CNAME
  Value: nivedh-portfolio.netlify.app
  TTL: 300
  ```

---

## 📊 Section 2: Free Web Analytics Integration

* **Analytics Provider:** **GoatCounter Analytics** (Privacy-focused, lightweight, zero-cookie tracking).
* **Dashboard URL:** `https://nivedh-portfolio.goatcounter.com`
* **Embedded Script Tag in `<head>`:**
  ```html
  <script data-goatcounter="https://nivedh-portfolio.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
  ```
* **Metrics Verified:** Real-time visitor counts, pageview hits, session duration, referrers, and browser/device breakdown.

---

## 🧼 Section 3: Launch Hygiene Checklist

| Hygiene Requirement | Implementation Status | Evidence / Verification |
| :--- | :--- | :--- |
| **Page Title** | `Nivedh — Systems & Backend Engineering Portfolio` | Clean browser tab title across all pages. |
| **SVG Favicon** | Inline SVG brand logo embedded in `<head>` | Displays 40x40 dark blue brand mark in browser tab. |
| **Social Share Previews** | Open Graph & Twitter Cards (`og:title`, `og:image`, `twitter:card`) | Verified rich link previews when sharing on LinkedIn, Twitter, and Slack. |
| **Mobile Responsiveness** | Verified on iPhone Safari / Android Chrome (375px viewport) | Enforced 48px touch targets, zero horizontal scroll, clean font scaling. |

---

## ⚡ Section 4: FlyRank Graduate Verification Badge

Installed the official **FlyRank Graduate Verification Badge** in the site footer:

```html
<div class="flyrank-badge-container">
  <a href="https://flyrank.ai/verify/nivedh" target="_blank" rel="noopener noreferrer" class="flyrank-badge" aria-label="FlyRank Graduate Verification Badge">
    <span class="badge-icon">⚡</span> Verified FlyRank AI Graduate — General AI Fluency & Backend Engineering
  </a>
</div>
```

---

## 🔄 Pass / Revise Checklist
* [x] **Live Custom Domain / Subdomain:** HTTPS SSL active on `https://nivedh-portfolio.netlify.app`.
* [x] **Free Analytics Working:** GoatCounter analytics script installed and tracking.
* [x] **Launch Hygiene Verified:** Social share previews, SVG favicon, titles, and mobile layout confirmed.
* [x] **FlyRank Badge Installed:** Visible in site footer linking to verification page.
