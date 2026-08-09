# 🌐 PF-04: Personal Website & DNS Walkthrough

**Track:** General AI Fluency (Week 5)  
**Deliverable:** Live HTTPS Netlify URL & Plain-Language DNS / CNAME Technical Walkthrough  

---

## 🚀 1. Live HTTPS Website & Positioning

* **Live HTTPS URL:** [https://nivedh-portfolio.netlify.app](https://nivedh-portfolio.netlify.app)
* **SSL Certificate:** Verified active HTTPS padlock served via Let's Encrypt / Netlify SSL.
* **GitHub Repository:** [https://github.com/NivedhN160/flyrank-internship](https://github.com/NivedhN160/flyrank-internship)

### Required Links & Positioning Verification
* **One-Line Claim:** *"I build resilient, production-ready software from bare-metal C kernels to Dockerized FastAPI backends—and here is the verifiable code to prove it."*
* **GitHub Link:** [https://github.com/NivedhN160](https://github.com/NivedhN160)
* **LinkedIn Profile:** [https://www.linkedin.com/in/nivedhn160/](https://www.linkedin.com/in/nivedhn160/)
* **CV / Proof Statement:** [https://github.com/NivedhN160/flyrank-internship/blob/main/week%201/Proof_Statement.md](https://github.com/NivedhN160/flyrank-internship/blob/main/week%201/Proof_Statement.md)
* **Contact / Booking:** `mailto:nivedhn160@gmail.com`

---

## 📖 2. Plain-Language DNS Walkthrough (For Non-Technical Teammates)

### What is DNS? (The Internet's Phonebook)
Computers communicate using numerical IP addresses like `192.0.2.1` or `104.198.14.52`. However, humans remember names like `nivedh-portfolio.netlify.app` or `nivedh.flyrank.ai`. 

The **Domain Name System (DNS)** is the global lookup network that translates human-readable domain names into machine-readable IP addresses in milliseconds.

---

### What Happens When Someone Types `nivedh.flyrank.ai`?

```text
[ User Browser ]
       │ 1. "Where is nivedh.flyrank.ai?"
       ▼
[ Recursive Resolver (ISP / 8.8.8.8) ]
       │ 2. Asks Root Nameserver (.) ──▶ Points to .ai TLD
       │ 3. Asks .ai TLD Server ─────▶ Points to FlyRank Authoritative DNS
       │ 4. Asks FlyRank DNS ────────▶ Returns CNAME "nivedh-portfolio.netlify.app"
       ▼
[ Netlify Edge Server ] ──▶ Returns IP & Serves Website Content over HTTPS
```

1. **Browser Cache Check:** The browser checks if it already knows the address for `nivedh.flyrank.ai`.
2. **Recursive Resolver Query:** If not cached, your browser contacts a Recursive Resolver (usually provided by your ISP or services like Google `8.8.8.8` or Cloudflare `1.1.1.1`).
3. **Root Nameserver Check:** The resolver asks the global Root Server (`.`), which directs it to the `.ai` Top-Level Domain (TLD) server.
4. **TLD Nameserver Check:** The `.ai` TLD server points to FlyRank's Authoritative Nameserver.
5. **Authoritative Nameserver Answer:** FlyRank's DNS server checks its record table and finds a **CNAME record** for `nivedh`. It responds: *"nivedh.flyrank.ai is an alias for nivedh-portfolio.netlify.app."*
6. **Netlify Edge Response:** The resolver fetches the IP for `nivedh-portfolio.netlify.app` from Netlify, and your browser loads the website over secure HTTPS.

---

### What is a CNAME Record? (The Domain Alias)
A **CNAME (Canonical Name)** record is a DNS record that points one domain name to another domain name instead of a static numerical IP address.

* **Example:** `nivedh.flyrank.ai` `CNAME` `nivedh-portfolio.netlify.app`
* **Why it matters:** Using a CNAME means if Netlify changes their underlying server IP addresses, your website never breaks—FlyRank's CNAME alias automatically follows Netlify's target domain.

---

## 📋 3. Capstone Subdomain Setup Checklist

When your `nivedh.flyrank.ai` subdomain is granted upon capstone approval, follow this exact checklist:

- [ ] **Step 1:** Log in to Netlify Dashboard and select `nivedh-portfolio`.
- [ ] **Step 2:** Navigate to **Site Configuration → Domain Management → Custom Domains**.
- [ ] **Step 3:** Click **Add custom domain** and enter `nivedh.flyrank.ai`.
- [ ] **Step 4:** Confirm that FlyRank Ops has created the `CNAME` record pointing `nivedh.flyrank.ai` to `nivedh-portfolio.netlify.app`.
- [ ] **Step 5:** Wait for DNS propagation (usually 1–5 minutes).
- [ ] **Step 6:** Click **Verify DNS configuration** in Netlify to automatically provision Let's Encrypt SSL/TLS.
- [ ] **Step 7:** Open `https://nivedh.flyrank.ai` in an incognito window and verify the secure padlock icon 🔒.

---

## 🔄 Pass / Revise Checklist
* [x] **Live HTTPS Site:** Deployed on clean domain `https://nivedh-portfolio.netlify.app`.
* [x] **Required Content Present:** Includes positioning claim, working links to LinkedIn, GitHub, CV/Proof Statement, and Contact email.
* [x] **Technically Correct DNS Walkthrough:** Plain-language explanation of DNS resolution, CNAME records, and IP lookups.
* [x] **Capstone Checklist Ready:** Prepped 7-step checklist for provisioning `nivedh.flyrank.ai`.
