import os
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status, Query
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from repository import get_repository, TaskRepository

load_dotenv()

repo: Optional[TaskRepository] = None

def get_repo_instance() -> TaskRepository:
    global repo
    if repo is None:
        repo = get_repository()
    return repo

def check_redis_status() -> str:
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    try:
        import redis
        r = redis.Redis.from_url(redis_url, socket_connect_timeout=1)
        r.ping()
        return "connected"
    except Exception:
        return "not_connected (optional stretch goal)"

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_repo_instance()
    yield

app = FastAPI(
    title="Task API (Postgres in Docker & Repository Pattern)",
    description="A CRUD API demonstrating storage layer swapping from SQLite to Postgres in Docker using the Repository Pattern. All API routes remain 100% unchanged.",
    version="3.0.0",
    lifespan=lifespan
)

@app.get(
    "/",
    summary="Root API Information",
    description="Returns metadata about the Task API and available endpoints."
)
def read_root():
    return {
        "name": "Task API (Postgres Repository)",
        "version": "3.0",
        "endpoints": ["/tasks", "/health", "/stats", "/reset"]
    }

@app.get(
    "/health",
    summary="Health Check (with Redis Ping)",
    description="Returns server status ok, current active database repository, and Redis ping connectivity."
)
def health_check():
    r = get_repo_instance()
    db_type = "PostgreSQL" if type(r).__name__ == "PostgresTaskRepository" else "SQLite (Fallback)"
    redis_state = check_redis_status()
    return {
        "status": "ok",
        "repository": db_type,
        "redis_status": redis_state
    }

@app.get(
    "/stats",
    summary="Task Statistics",
    description="Computes task totals, done count, and open count via repository data layer."
)
def get_task_stats():
    return get_repo_instance().get_stats()

@app.post(
    "/reset",
    summary="Reset Task Database",
    description="Resets table data back to the initial 3 seed tasks via repository data layer."
)
def reset_database():
    reset_tasks = get_repo_instance().reset()
    return {"message": "Database reset to initial 3 seed tasks", "tasks": reset_tasks}

@app.get(
    "/tasks",
    summary="List all tasks (with filtering & search)",
    description="Retrieve all tasks. Supports optional query parameters for filtering by completion status (?done=true) and searching by title keyword (?search=milk)."
)
def get_all_tasks(
    done: Optional[bool] = Query(None, description="Filter tasks by completion status"),
    search: Optional[str] = Query(None, description="Search task titles by keyword")
):
    return get_repo_instance().get_all(done=done, search=search)

@app.get(
    "/tasks/{task_id}",
    summary="Get a single task by ID",
    description="Retrieve task by primary key ID. Returns HTTP 404 Not Found if missing."
)
def get_single_task(task_id: int):
    task = get_repo_instance().get_by_id(task_id)
    if not task:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    return task

@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Insert a new task. Requires a non-empty title string."
)
async def create_task(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid or missing JSON body"}
        )
    
    if not isinstance(data, dict) or "title" not in data:
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )
    
    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )
    
    new_task = get_repo_instance().create(title.strip())
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=new_task
    )

@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Update title and/or done status for an existing task."
)
async def update_task(task_id: int, request: Request):
    r = get_repo_instance()
    existing = r.get_by_id(task_id)
    if not existing:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
        
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid or missing JSON body"}
        )
        
    if not isinstance(data, dict):
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must be a JSON object"}
        )

    title = None
    if "title" in data:
        t = data["title"]
        if not isinstance(t, str) or not t.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )
        title = t.strip()
        
    done = None
    if "done" in data:
        d = data["done"]
        if not isinstance(d, bool):
            return JSONResponse(
                status_code=400,
                content={"error": "done field must be a boolean"}
            )
        done = d

    updated = r.update(task_id, title=title, done=done)
    return updated

@app.delete(
    "/tasks/{task_id}",
    summary="Delete a task",
    description="Remove a task by ID. Returns HTTP 204 No Content on success."
)
def delete_task(task_id: int):
    r = get_repo_instance()
    success = r.delete(task_id)
    if not success:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
