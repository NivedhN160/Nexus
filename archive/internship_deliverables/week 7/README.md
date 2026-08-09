# 📄 Week 7 (BE-07): Automated PDF Report Generator

**Track:** Backend AI Engineering (Week 7)  
**Assignment:** BE-07 · PDF Report Generator  
**Architecture:** Data Aggregation Engine → Asynchronous PDF Worker Queue → ReportLab Rendering → Downloadable PDF Artifact  

---

## 🎯 System Architecture

In SaaS applications, generating PDF reports on large datasets is a classic heavy operation. This service offloads PDF compilation to an asynchronous background worker using the **HTTP 202 Accepted** pattern:

```text
[ Client Request ] ─────▶ POST /reports ──────────▶ HTTP 202 Accepted Fast
                                  │                 (job_id, download_url)
                                  ▼
                     [ Enqueue PDF Report Job ]
                                  │
                                  ▼
                [ Background PDF Worker Thread ]
                ├── 1. Data Aggregator (JSON / SQL Query)
                ├── 2. Calculates Metrics (Authors, Tags, Lengths)
                ├── 3. ReportLab Canvas & Table Flowables
                └── 4. Writes File: reports/report_{job_id}.pdf
                                  │
[ Client Polling ] ─────▶ GET /reports/{id} ──────▶ Status: "completed"
[ Client Download ] ────▶ GET /reports/{id}/download ▶ FileResponse (PDF binary stream)
```

---

## 🛠️ Components Built in `week 7/`

1. **Data Aggregator (`report_aggregator.py`):** Loads quotes dataset from `week 5/data/scraped_quotes.json`, aggregates author distributions, calculates top tags frequency, and computes character length statistics.
2. **ReportLab PDF Engine (`pdf_builder.py`):** Renders styled PDF reports featuring document titles, executive metric tables, author leaderboards, tag badges, and sample quote flowables.
3. **Background Worker (`job_worker.py`):** Manages async thread execution, job status (`pending` → `processing` → `completed`), retry counters, and artifact storage.
4. **FastAPI Application (`main.py`):** Exposes `POST /reports`, `GET /reports/{job_id}`, `GET /reports/{job_id}/download`, `GET /reports`, and `GET /health`.

---

## 🧪 Verification & Test Logs

Run the end-to-end test suite verifying PDF generation and binary download:

```bash
powershell -Command "Set-Location 'E:\Flyrank internship\week 7'; .\venv\Scripts\python 'C:\Users\nived\.gemini\antigravity-cli\brain\960f87be-2bb8-4ec7-9a9a-c0c6864012d0\scratch\test_w7_endpoints.py'"
```

### Verified Test Log Output
```text
=== 1. GET /health ===
HTTP 200: {"status":"ok","worker_running":true,"total_reports_generated":0}

=== 2. POST /reports (Requesting PDF Report - HTTP 202 Fast Accept) ===
HTTP 202: {"message":"PDF Report generation accepted and enqueued in background","job_id":"34b42041-f882-4daf-a800-b2e86b8381ad","status":"pending","download_url":"/reports/34b42041-f882-4daf-a800-b2e86b8381ad/download"}

=== 5. GET /reports/34b42041-f882-4daf-a800-b2e86b8381ad (Polling After Completion) ===
HTTP 200: {"job_id":"34b42041-f882-4daf-a800-b2e86b8381ad","status":"completed","progress":100,"file_path":"reports\\report_34b42041-f882-4daf-a800-b2e86b8381ad.pdf"}

=== 6. GET /reports/34b42041-f882-4daf-a800-b2e86b8381ad/download (Downloading PDF Artifact) ===
HTTP 200: Received PDF File! Content-Type: application/pdf, Size: 2637 bytes

[SUCCESS] PDF REPORT GENERATION VERIFIED PERFECTLY!
```
