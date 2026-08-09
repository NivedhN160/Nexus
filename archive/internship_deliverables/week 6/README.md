# ⚙️ Week 6 (BE-06): Your First Background Job

**Track:** Backend AI Engineering (Week 6)  
**Assignment:** BE-06 · Your First Background Job  
**Architecture:** Fast Accept (HTTP 202) → Asynchronous Worker Queue → Polling Status Endpoint  

---

## 🎯 Architecture Overview

In modern production systems, slow operations (such as AI text generation, vector embedding, or scraping pipelines) must **never** block synchronous HTTP request-response threads. 

This repository implements the industry-standard **Accept Fast, Work in Background, Report Status** pattern:

```text
[ Client Request ] ──────▶ POST /jobs ──────────▶ Return HTTP 202 Accepted Fast
                                  │                (job_id, status_url)
                                  ▼
                        [ Enqueue in Worker Queue ]
                                  │
                                  ▼
                   [ Async Background Worker Loop ]
                   ├── Idempotency Check (Prevents Duplicate Run)
                   ├── Execution Loop & Progress Updates (25% → 100%)
                   ├── Automatic Retries on Failure (Attempts 1 → 2 → 3)
                   └── Permanent Failure Alerting (Slack/Email Log)
                                  │
[ Client Polling ] ──────▶ GET /jobs/{job_id} ──▶ Returns Status & Final Result
```

---

## 🔒 Non-Negotiable Engineering Requirements

### 1. Idempotency (Duplicate Prevention)
* **Rule:** A job submitted with the same `idempotency_key` must **never** be executed twice.
* **Implementation:** The `JobManager` maintains an atomic `idempotency_map`. If a key is re-submitted, the API immediately returns `HTTP 202 Accepted` with `"is_duplicate": true` and points to the existing `job_id`.

### 2. Retries & Exponential Backoff
* **Rule:** Transient network/service failures automatically trigger retries before failing.
* **Implementation:** If a job fails during execution, the worker increments `attempts` (up to `max_attempts = 3`), resets status to `pending`, applies backoff delay, and re-queues the job.

### 3. Failure Alerts
* **Rule:** If a job exhausts all retries, the system must trigger an alert.
* **Implementation:** When `attempts >= max_attempts`, the worker marks status as `failed` and emits a high-priority alert log: `[ERROR] ALERT !!! JOB FAILED PERMANENTLY: Job exhausted all 3 retries.`

---

## 🚀 API Endpoint Reference

| Method | Endpoint | HTTP Status | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | `200 OK` | Worker health status and queue metrics. |
| `POST` | `/jobs` | `202 Accepted` | Enqueues background job fast; returns `job_id` and `status_url`. |
| `GET` | `/jobs/{job_id}` | `200 OK` / `404` | Polling endpoint returning job status, progress %, attempts, and results. |
| `GET` | `/jobs` | `200 OK` | Lists all enqueued, processing, completed, and failed jobs. |

---

## 🧪 Verification & Test Logs

Run the comprehensive test suite verifying 202 fast acceptance, polling, idempotency, retries, and alert logging:

```bash
powershell -Command "Set-Location 'E:\Flyrank internship\week 6'; .\venv\Scripts\python 'C:\Users\nived\.gemini\antigravity-cli\brain\960f87be-2bb8-4ec7-9a9a-c0c6864012d0\scratch\test_w6_endpoints.py'"
```

### Verified Test Log Output
```text
=== 1. GET /health ===
HTTP 200: {"status":"ok","worker_running":true,"queue_metrics":{"total_jobs":0,"pending":0,"processing":0,"completed":0,"failed":0}}

=== 2. POST /jobs (HTTP 202 Accepted Fast) ===
HTTP 202: {"message":"Job accepted and enqueued for background processing","job_id":"57b28db7-544a-41cc-b39a-ee088aa2ae4b","status":"pending","is_duplicate":false}

=== 4. Testing Idempotency (Submitting Duplicate Request) ===
HTTP 202: {"message":"Duplicate request detected — returning existing job status","job_id":"57b28db7-544a-41cc-b39a-ee088aa2ae4b","is_duplicate":true}

=== 6. GET /jobs/{job_id} (Polling Status After Completion) ===
HTTP 200: {"job_id":"57b28db7-544a-41cc-b39a-ee088aa2ae4b","status":"completed","progress":100,"attempts":1,"result":{"summary":"Synthesized AI response","tokens_processed":1420}}

=== 7. Testing Failure, Retries & Alerts (Submitting Failing Job) ===
2026-08-05 20:04:40,730 [WARNING] JOB RETRY: Job failed attempt 1. Re-enqueuing...
2026-08-05 20:04:42,433 [WARNING] JOB RETRY: Job failed attempt 2. Re-enqueuing...
2026-08-05 20:04:44,136 [ERROR] ALERT !!! JOB FAILED PERMANENTLY: Job exhausted all 3 retries. Sending Slack/Email Alert!
```
