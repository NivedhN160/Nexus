"""
AI-generated version of Task API (Stage 7 Rematch)
Generated from memory prompt asking for FastAPI Task CRUD API.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title="Task API (AI Version)",
    description="AI-generated to-do list CRUD API",
    version="1.0.0"
)

class TaskItem(BaseModel):
    id: int
    title: str
    done: bool = False

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Title of task")

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    done: Optional[bool] = None

# Initial database
db: List[dict] = [
    {"id": 1, "title": "Setup development environment", "done": True},
    {"id": 2, "title": "Watch request-response lecture", "done": True},
    {"id": 3, "title": "Build CRUD API for Week 2", "done": False},
]

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def list_tasks():
    return db

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for item in db:
        if item["id"] == task_id:
            return item
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    new_id = max([t["id"] for t in db], default=0) + 1
    new_item = {"id": new_id, "title": payload.title.strip(), "done": False}
    db.append(new_item)
    return new_item

@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate):
    for item in db:
        if item["id"] == task_id:
            if payload.title is not None:
                item["title"] = payload.title.strip()
            if payload.done is not None:
                item["done"] = payload.done
            return item
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for idx, item in enumerate(db):
        if item["id"] == task_id:
            db.pop(idx)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
