import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse, FileResponse
from dotenv import load_dotenv

from job_worker import PDFJobManager, ReportRequestPayload, JobStatus

load_dotenv()

pdf_job_manager = PDFJobManager(reports_dir="reports")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("FastAPI Automated PDF Report Generator running.")
    yield

app = FastAPI(
    title="Automated PDF Report Generator API",
    description="Asynchronous PDF report generation pipeline using HTTP 202 Accepted fast response, Data Aggregation, and ReportLab PDF document rendering.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get(
    "/",
    summary="Root Endpoint",
    description="Returns service metadata and endpoints."
)
def read_root():
    return {
        "name": "Automated PDF Report Generator",
        "pattern": "Fast Accept (HTTP 202) -> Data Aggregation -> PDF Rendering -> Artifact Link",
        "endpoints": ["POST /reports", "GET /reports/{job_id}", "GET /reports/{job_id}/download", "GET /reports", "GET /health"]
    }

@app.get(
    "/health",
    summary="Health & Queue Status"
)
def health_check():
    jobs = pdf_job_manager.list_jobs()
    completed = sum(1 for j in jobs if j.status == JobStatus.COMPLETED)
    return {
        "status": "ok",
        "worker_running": pdf_job_manager.is_running,
        "total_reports_generated": completed
    }

@app.post(
    "/reports",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Generate PDF Report (HTTP 202 Accepted)",
    description="Enqueues background PDF report generation instantly and returns HTTP 202 Accepted with status URL and download URL."
)
def request_pdf_report(payload: ReportRequestPayload, response: Response):
    job_record = pdf_job_manager.enqueue_report_job(payload)
    response.status_code = status.HTTP_202_ACCEPTED
    
    return {
        "message": "PDF Report generation accepted and enqueued in background",
        "job_id": job_record.job_id,
        "status": job_record.status,
        "status_url": f"/reports/{job_record.job_id}",
        "download_url": f"/reports/{job_record.job_id}/download"
    }

@app.get(
    "/reports/{job_id}",
    summary="Get Report Job Status (Polling Endpoint)"
)
def get_report_status(job_id: str):
    job = pdf_job_manager.get_job(job_id)
    if not job:
        return JSONResponse(status_code=404, content={"error": f"Report job {job_id} not found"})
    return job

@app.get(
    "/reports/{job_id}/download",
    summary="Download Generated PDF Report"
)
def download_pdf_report(job_id: str):
    job = pdf_job_manager.get_job(job_id)
    if not job:
        return JSONResponse(status_code=404, content={"error": f"Report job {job_id} not found"})
    
    if job.status != JobStatus.COMPLETED or not job.file_path:
        return JSONResponse(
            status_code=400,
            content={"error": f"PDF report is not ready yet. Current status: {job.status}"}
        )
    
    if not os.path.exists(job.file_path):
        return JSONResponse(status_code=404, content={"error": f"PDF file not found on disk at {job.file_path}"})

    return FileResponse(
        path=job.file_path,
        media_type="application/pdf",
        filename=f"Backend_Analytics_Report_{job_id[:8]}.pdf"
    )

@app.get(
    "/reports",
    summary="List All PDF Reports"
)
def list_reports():
    return pdf_job_manager.list_jobs()
