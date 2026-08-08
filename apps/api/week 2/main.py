from typing import Optional
from fastapi import FastAPI, Request, Response, status, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="Task API",
    description="A CRUD API for managing a to-do list built with FastAPI.",
    version="1.0.0"
)

# Initial seed dataset
INITIAL_TASKS = [
    {"id": 1, "title": "Setup development environment", "done": True},
    {"id": 2, "title": "Watch request-response lecture", "done": True},
    {"id": 3, "title": "Build CRUD API for Week 2", "done": False},
]

# In-memory database
tasks_db = [dict(t) for t in INITIAL_TASKS]

# Pydantic Schemas for Swagger UI documentation
class TaskCreateSchema(BaseModel):
    title: str = Field(..., example="Buy milk", description="Title of the task")

class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, example="Buy almond milk", description="Updated title of the task")
    done: Optional[bool] = Field(None, example=True, description="Completion status of the task")

@app.get(
    "/",
    summary="Root API Information",
    description="Returns metadata about the Task API and available primary endpoints."
)
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/health", "/stats", "/reset"]
    }

@app.get(
    "/health",
    summary="Health Check",
    description="Returns status ok if the server is running properly."
)
def health_check():
    return {"status": "ok"}

@app.get(
    "/stats",
    summary="Task Statistics",
    description="Calculates and returns total, done, and open tasks counts."
)
def get_task_stats():
    total = len(tasks_db)
    done_count = sum(1 for t in tasks_db if t["done"])
    open_count = total - done_count
    return {
        "total": total,
        "done": done_count,
        "open": open_count
    }

@app.post(
    "/reset",
    summary="Reset Task Database",
    description="Restores the in-memory database to the original 3 seed tasks."
)
def reset_database():
    global tasks_db
    tasks_db = [dict(t) for t in INITIAL_TASKS]
    return {"message": "Database reset to initial 3 tasks", "tasks": tasks_db}

@app.get(
    "/tasks",
    summary="List all tasks (with optional filtering & search)",
    description="Retrieve all tasks in the list. Supports query parameters for filtering by completion status (?done=true) or searching by title keyword (?search=milk)."
)
def get_all_tasks(
    done: Optional[bool] = Query(None, description="Filter tasks by completion status"),
    search: Optional[str] = Query(None, description="Search tasks by title keyword")
):
    filtered = tasks_db
    if done is not None:
        filtered = [t for t in filtered if t["done"] == done]
    if search:
        search_term = search.lower().strip()
        filtered = [t for t in filtered if search_term in t["title"].lower()]
    return filtered

@app.get(
    "/tasks/{task_id}",
    summary="Get a single task by ID",
    description="Retrieve specific task details by ID. Returns 404 if the task ID does not exist."
)
def get_single_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )

@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Add a new task to the list. Automatically assigns the next ID and sets done to false. Requires a non-empty title."
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
    
    next_id = max([t["id"] for t in tasks_db], default=0) + 1
    new_task = {
        "id": next_id,
        "title": title.strip(),
        "done": False
    }
    tasks_db.append(new_task)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=new_task
    )

@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Modify title and/or done status for an existing task. Returns 404 if task ID doesn't exist, or 400 for invalid body."
)
async def update_task(task_id: int, request: Request):
    target_task = None
    for task in tasks_db:
        if task["id"] == task_id:
            target_task = task
            break
            
    if not target_task:
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

    if "title" in data:
        title = data["title"]
        if not isinstance(title, str) or not title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )
        target_task["title"] = title.strip()
        
    if "done" in data:
        if not isinstance(data["done"], bool):
            return JSONResponse(
                status_code=400,
                content={"error": "done field must be a boolean"}
            )
        target_task["done"] = data["done"]

    return target_task

@app.delete(
    "/tasks/{task_id}",
    summary="Delete a task",
    description="Remove a task by ID. Returns HTTP 204 No Content on success, or 404 if task ID is not found."
)
def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
            
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )
