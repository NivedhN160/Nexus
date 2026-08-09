import os
import time
import uuid
import logging
import threading
from enum import Enum
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Field

from report_aggregator import DataAggregator
from pdf_builder import PDFReportGenerator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("PDFWorker")

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ReportRequestPayload(BaseModel):
    report_title: Optional[str] = Field("Backend AI Data Analytics Report", example="Weekly Scraper Analytics Report")
    data_source_path: Optional[str] = Field("../week 5/data/scraped_quotes.json", example="../week 5/data/scraped_quotes.json")

class PDFJobRecord(BaseModel):
    job_id: str
    report_title: str
    status: JobStatus
    progress: int = 0
    attempts: int = 0
    max_attempts: int = 3
    created_at: str
    completed_at: Optional[str] = None
    file_path: Optional[str] = None
    download_url: Optional[str] = None
    error: Optional[str] = None

class PDFJobManager:
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
        self.jobs: Dict[str, PDFJobRecord] = {}
        self.lock = threading.Lock()
        self.pdf_generator = PDFReportGenerator(output_dir=self.reports_dir)
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.is_running = True
        self.worker_thread.start()
        logger.info("PDF Report Generator Background Worker started successfully.")

    def enqueue_report_job(self, payload: ReportRequestPayload) -> PDFJobRecord:
        with self.lock:
            job_id = str(uuid.uuid4())
            record = PDFJobRecord(
                job_id=job_id,
                report_title=payload.report_title or "Backend AI Data Analytics Report",
                status=JobStatus.PENDING,
                created_at=datetime.now().isoformat()
            )
            self.jobs[job_id] = record
            logger.info(f"REPORT JOB ACCEPTED FAST [202 Accepted]: Enqueued Job ID '{job_id}'")
            return record

    def get_job(self, job_id: str) -> Optional[PDFJobRecord]:
        with self.lock:
            return self.jobs.get(job_id)

    def list_jobs(self) -> List[PDFJobRecord]:
        with self.lock:
            return list(self.jobs.values())

    def _worker_loop(self):
        while self.is_running:
            target_job_id = None
            with self.lock:
                for j_id, job in self.jobs.items():
                    if job.status == JobStatus.PENDING:
                        target_job_id = j_id
                        break
            
            if not target_job_id:
                time.sleep(0.2)
                continue

            self._process_pdf_job(target_job_id)

    def _process_pdf_job(self, job_id: str):
        with self.lock:
            job = self.jobs.get(job_id)
            if not job:
                return
            job.status = JobStatus.PROCESSING
            job.attempts += 1
            job.progress = 20

        logger.info(f"WORKER RENDERING PDF: Job '{job_id}' (Attempt {job.attempts}/3)")

        try:
            # 1. Aggregate Data
            time.sleep(0.5)
            aggregator = DataAggregator(json_file_path="../week 5/data/scraped_quotes.json")
            metrics = aggregator.generate_summary_metrics()

            with self.lock:
                job.progress = 60

            # 2. Render PDF Report via ReportLab
            time.sleep(0.5)
            pdf_path = self.pdf_generator.generate_pdf(job_id, metrics, title=job.report_title)

            # 3. Complete Job
            with self.lock:
                job.status = JobStatus.COMPLETED
                job.progress = 100
                job.completed_at = datetime.now().isoformat()
                job.file_path = pdf_path
                job.download_url = f"/reports/{job_id}/download"

            logger.info(f"PDF GENERATED SUCCESS: Report saved to '{pdf_path}'")

        except Exception as e:
            logger.error(f"PDF RENDER ERROR: {str(e)}")
            with self.lock:
                if job.attempts < job.max_attempts:
                    job.status = JobStatus.PENDING  # Retry
                else:
                    job.status = JobStatus.FAILED
                    job.error = str(e)
