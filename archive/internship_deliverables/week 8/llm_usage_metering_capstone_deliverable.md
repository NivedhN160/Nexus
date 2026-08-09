# 💳 LLM Usage Metering & Billing Service Capstone Deliverable

**Capstone Title:** LLM Usage Metering & Billing Service  
**Track:** Backend AI Engineering Capstone  
**Author:** Nivedh  
**Dedicated GitHub Repository:** [https://github.com/NivedhN160/LLM-Usage-Metering-Billing-Service-Flyrank-Capstone](https://github.com/NivedhN160/LLM-Usage-Metering-Billing-Service-Flyrank-Capstone)  
**Evaluator Manifest:** `capstone.yaml`  

---

## 📌 Submission Pack Files (§ 11)

1. **`README.md`:** [https://github.com/NivedhN160/LLM-Usage-Metering-Billing-Service-Flyrank-Capstone/blob/main/README.md](https://github.com/NivedhN160/LLM-Usage-Metering-Billing-Service-Flyrank-Capstone/blob/main/README.md)  
   Complete system architecture diagram, setup instructions, API documentation, Money Math & Token Pricing rules, and limitations note.
2. **`capstone.yaml`:** Evaluator manifest specifying `run:`, `seed:`, `test:`, `base_url:`, and probe endpoints.
3. **`EVIDENCE.md`:** Verification transcripts and Pytest probe evidence for every Definition-of-Done checkbox (§ 6).
4. **`BUILDLOG.md`:** AI collaboration log detailing prompt assistance, refactoring choices, and bug fixes.
5. **`.env.example`:** Safe environment variable configuration template.

---

## 🧪 Acceptance Probe Verification Results (§ 12)

All 5 evaluator acceptance probes pass with 100% green status:

```text
test_suite.py::test_probe_1_idempotent_no_double_count PASSED            [ 20%]
test_suite.py::test_probe_2_quota_boundary_enforcement PASSED            [ 40%]
test_suite.py::test_probe_3_stripe_test_checkout_upgrade PASSED          [ 60%]
test_suite.py::test_probe_4_forged_and_replayed_webhook_handling PASSED  [ 80%]
test_suite.py::test_probe_5_pinned_token_pricing_rules PASSED            [100%]

======================= 5 passed in 0.86s =======================
```

---

## 📝 Portal Submission Format

```text
Backend AI Engineering Track Capstone Submission
Project: LLM Usage Metering & Billing Service

1. Dedicated GitHub Repository: https://github.com/NivedhN160/LLM-Usage-Metering-Billing-Service-Flyrank-Capstone
2. Evaluator Manifest (capstone.yaml): https://github.com/NivedhN160/LLM-Usage-Metering-Billing-Service-Flyrank-Capstone/blob/main/capstone.yaml
3. Verification Evidence (EVIDENCE.md): https://github.com/NivedhN160/LLM-Usage-Metering-Billing-Service-Flyrank-Capstone/blob/main/EVIDENCE.md
4. Architecture & Setup README: https://github.com/NivedhN160/LLM-Usage-Metering-Billing-Service-Flyrank-Capstone/blob/main/README.md
5. Build & AI Usage Log (BUILDLOG.md): https://github.com/NivedhN160/LLM-Usage-Metering-Billing-Service-Flyrank-Capstone/blob/main/BUILDLOG.md
```
