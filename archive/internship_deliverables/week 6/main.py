import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, status, Query
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from job_queue import JobManager, JobPayload, JobStatus

load_dotenv()

job_manager = JobManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("FastAPI Server running with Background Worker Thread active.")
    yield

app = FastAPI(
    title="Async Job Queue API (HTTP 202 Pattern & Worker Architecture)",
    description="A production-grade asynchronous backend service implementing the HTTP 202 Accepted pattern, background worker processing, idempotency checks, automatic retries with exponential backoff, and failure alerts.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get(
    "/",
    summary="Root Endpoint",
    description="Returns service metadata and available background job endpoints."
)
def read_root():
    return {
        "name": "Async Background Job API",
        "version": "1.0",
        "pattern": "Accept Fast (202), Work in Background, Poll Status",
        "endpoints": ["POST /jobs", "GET /jobs/{job_id}", "GET /jobs", "GET /health"]
    }

@app.get(
    "/health",
    summary="Health & Queue Status",
    description="Returns worker status and queue metrics."
)
def health_check():
    jobs = job_manager.list_jobs()
    pending = sum(1 for j in jobs if j.status == JobStatus.PENDING)
    processing = sum(1 for j in jobs if j.status == JobStatus.PROCESSING)
    completed = sum(1 for j in jobs if j.status == JobStatus.COMPLETED)
    failed = sum(1 for j in jobs if j.status == JobStatus.FAILED)
    
    return {
        "status": "ok",
        "worker_running": job_manager.is_running,
        "queue_metrics": {
            "total_jobs": len(jobs),
            "pending": pending,
            "processing": processing,
            "completed": completed,
            "failed": failed
        }
    }

@app.post(
    "/jobs",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Enqueue Async Background Job (202 Accepted)",
    description="Accepts slow task requests instantly (HTTP 202 Accepted) and hands execution to background worker thread. Enforces idempotency via optional idempotency_key."
)
def create_background_job(payload: JobPayload, response: Response):
    job_record, is_duplicate = job_manager.enqueue_job(payload)
    
    response.status_code = status.HTTP_202_ACCEPTED
    
    return {
        "message": "Job accepted and enqueued for background processing" if not is_duplicate else "Duplicate request detected — returning existing job status",
        "job_id": job_record.job_id,
        "idempotency_key": job_record.idempotency_key,
        "status": job_record.status,
        "is_duplicate": is_duplicate,
        "status_url": f"/jobs/{job_record.job_id}"
    }

@app.get(
    "/jobs/{job_id}",
    summary="Get Job Status (Polling Endpoint)",
    description="Polls job status by ID. Returns progress percentage, attempts count, and result when completed."
)
def get_job_status(job_id: str):
    job = job_manager.get_job(job_id)
    if not job:
        return JSONResponse(
            status_code=404,
            content={"error": f"Job {job_id} not found"}
        )
    return job

@app.get(
    "/jobs",
    summary="List All Background Jobs",
    description="Returns a list of all enqueued, processing, completed, and failed background jobs."
)
def list_all_jobs():
    return job_manager.list_jobs()
