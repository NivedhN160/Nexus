import time
import uuid
import logging
import threading
from enum import Enum
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BackgroundWorker")

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobPayload(BaseModel):
    task_type: str = Field(..., example="ai_synthesis")
    prompt: str = Field(..., example="Synthesize RAG corpus summary from Week 5 scraper")
    idempotency_key: Optional[str] = Field(None, example="key_unique_12345")
    simulate_failure: Optional[bool] = Field(False, description="Set True to test retry & alert worker logic")

class JobRecord(BaseModel):
    job_id: str
    idempotency_key: Optional[str] = None
    task_type: str
    prompt: str
    status: JobStatus
    progress: int = 0
    attempts: int = 0
    max_attempts: int = 3
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class JobManager:
    def __init__(self):
        self.jobs: Dict[str, JobRecord] = {}
        self.idempotency_map: Dict[str, str] = {}  # idempotency_key -> job_id
        self.lock = threading.Lock()
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.is_running = True
        self.worker_thread.start()
        logger.info("Background Worker Thread started successfully.")

    def enqueue_job(self, payload: JobPayload) -> Tuple[JobRecord, bool]:
        """
        Enqueues job fast. Returns (JobRecord, is_duplicate).
        Demonstrates Idempotency: If idempotency_key was already processed, returns existing job!
        """
        with self.lock:
            if payload.idempotency_key and payload.idempotency_key in self.idempotency_map:
                existing_id = self.idempotency_map[payload.idempotency_key]
                logger.warning(f"IDEMPOTENCY TRIGGERED: Key '{payload.idempotency_key}' already mapped to Job '{existing_id}'. Returning existing job.")
                return self.jobs[existing_id], True

            job_id = str(uuid.uuid4())
            record = JobRecord(
                job_id=job_id,
                idempotency_key=payload.idempotency_key,
                task_type=payload.task_type,
                prompt=payload.prompt,
                status=JobStatus.PENDING,
                created_at=datetime.now().isoformat(),
                max_attempts=3
            )
            
            self.jobs[job_id] = record
            if payload.idempotency_key:
                self.idempotency_map[payload.idempotency_key] = job_id
                
            logger.info(f"JOB ACCEPTED FAST [202 Accepted]: Enqueued Job ID '{job_id}' (Task: {payload.task_type})")
            return record, False

    def get_job(self, job_id: str) -> Optional[JobRecord]:
        with self.lock:
            return self.jobs.get(job_id)

    def list_jobs(self) -> List[JobRecord]:
        with self.lock:
            return list(self.jobs.values())

    def _worker_loop(self):
        """
        Background Worker Processing Loop:
        Picks pending jobs, updates status to processing, handles slow operation, retries on failure, sends alerts.
        """
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

            self._process_single_job(target_job_id)

    def _process_single_job(self, job_id: str):
        with self.lock:
            job = self.jobs.get(job_id)
            if not job:
                return
            job.status = JobStatus.PROCESSING
            job.started_at = datetime.now().isoformat()
            job.attempts += 1
            job.progress = 25
            current_attempt = job.attempts
            simulate_fail = "fail" in job.prompt.lower() or job.prompt.startswith("FAIL_TEST")

        logger.info(f"WORKER PROCESSING: Job '{job_id}' (Attempt {current_attempt}/{job.max_attempts})")

        # Simulate slow operation (1.5 seconds background work for test speed)
        for p in [50, 75, 90]:
            time.sleep(0.4)
            with self.lock:
                if job_id in self.jobs:
                    self.jobs[job_id].progress = p

        # Check for simulated failure vs success
        if simulate_fail and current_attempt < job.max_attempts:
            with self.lock:
                job.status = JobStatus.PENDING  # Re-enqueue for retry
                logger.warning(f"JOB RETRY: Job '{job_id}' failed attempt {current_attempt}. Re-enqueuing for retry...")
            time.sleep(0.5)  # Backoff delay
            return

        if simulate_fail and current_attempt >= job.max_attempts:
            with self.lock:
                job.status = JobStatus.FAILED
                job.completed_at = datetime.now().isoformat()
                job.error = f"Job failed after {job.max_attempts} attempts. Simulated failure condition."
                logger.error(f"ALERT !!! JOB FAILED PERMANENTLY: Job '{job_id}' exhausted all {job.max_attempts} retries. Sending Slack/Email Alert!")
            return

        # Success path
        with self.lock:
            job.status = JobStatus.COMPLETED
            job.progress = 100
            job.completed_at = datetime.now().isoformat()
            job.result = {
                "summary": f"Synthesized AI response for '{job.prompt}'",
                "tokens_processed": 1420,
                "confidence_score": 0.98,
                "execution_time_seconds": 1.8
            }
            logger.info(f"JOB COMPLETED SUCCESS: Job '{job_id}' finished successfully.")
