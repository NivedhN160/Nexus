# The Prompt Ladder: From Lazy Prompt to Engineered Spec
**Track:** General AI Fluency (Week 2)  
**Deliverable:** 6-Run Prompt Engineering Ladder & Analysis  

---

## 🪜 Overview
This document traces the systematic evolution of a backend development prompt across six iterations (Baseline + 5 Versions). Each step adds exactly one engineering layer to observe its specific effect on the AI model's output.

---

## 1. Baseline Run (The Lazy Prompt)

### 🔴 Baseline Prompt
> *"Write backend code for a todo app."*

### 📄 Representative Output Excerpt
```python
# A simple Flask todo app
from flask import Flask, jsonify, request

app = Flask(__name__)
todos = []

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    todos.append(request.json)
    return "Added", 200

if __name__ == '__main__':
    app.run()
```

### 📝 Baseline Reflection
* Generic, unvalidated Flask code.
* No status code standards (returns raw string "Added" with 200 instead of JSON object with 201 Created).
* No path parameters, error handling, or API documentation.

---

## 2. Version 1: Adding Layer 1 — Clear Goal & Tech Stack

### 🔵 Prompt v1 (Layer Added: Specific Tech Stack & Framework)
> *"Write backend code for a todo app using Python and FastAPI on port 8000."*

### 📄 Representative Output Excerpt
```python
from fastapi import FastAPI
app = FastAPI()

tasks = []

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: dict):
    tasks.append(task)
    return task
```

### 📋 Version 1 Notes
1. **What changed in prompt:** Specified Python and FastAPI on port 8000.
2. **What improved in output:** The framework switched from outdated Flask to modern FastAPI; automatic JSON serialization replaced manual `jsonify()`.
3. **What still failed:** The code lacks an in-memory data model (no task IDs), HTTP status codes are defaulted to 200 OK for creation, and there is no input validation or error handling.
4. **What to try next:** Add defined audience and project context.

---

## 3. Version 2: Adding Layer 2 — Target Audience & Context

### 🔵 Prompt v2 (Layer Added: Target Audience & Context)
> *"Write backend code for a todo app using Python and FastAPI on port 8000. This is for an entry-level backend engineering intern learning REST fundamentals, so keep data in memory (no external SQL database) and write clean, readable code."*

### 📄 Representative Output Excerpt
```python
from fastapi import FastAPI

app = FastAPI()

# Simple in-memory list with initial seed data
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": True},
    {"id": 2, "title": "Build CRUD API", "done": False}
]

@app.get("/tasks")
def list_tasks():
    return tasks

@app.post("/tasks")
def add_task(title: str):
    new_id = len(tasks) + 1
    new_task = {"id": new_id, "title": title, "done": False}
    tasks.append(new_task)
    return new_task
```

### 📋 Version 2 Notes
1. **What changed in prompt:** Specified intern audience context and required strictly in-memory data structures without external database dependencies.
2. **What improved in output:** The output introduced pre-filled seed data with an explicit task dictionary structure (`id`, `title`, `done`) and removed unwanted database installation instructions (`SQLAlchemy`/`PostgreSQL`).
3. **What still failed (Honest "Made it Worse" moment):** The endpoint signature changed to `add_task(title: str)` as a URL query parameter (`POST /tasks?title=Buy+milk`) instead of reading a JSON request body from HTTP POST payloads. This broke standard REST conventions.
4. **What to try next:** Specify exact output format, HTTP methods, endpoints, and JSON body structure.

---

## 4. Version 3: Adding Layer 3 — Specified Output Format & Endpoints

### 🔵 Prompt v3 (Layer Added: Specified Output Format & Endpoint Schema)
> *"Write backend code for a todo app using Python and FastAPI on port 8000. This is for an entry-level backend engineering intern learning REST fundamentals, so keep data in memory (no external SQL database). Implement five explicit endpoints: GET /, GET /health, GET /tasks, GET /tasks/{id}, POST /tasks (reading JSON body {"title": "..."}), PUT /tasks/{id}, and DELETE /tasks/{id}."*

### 📄 Representative Output Excerpt
```python
@app.post("/tasks")
def create_task(data: dict):
    new_id = len(tasks) + 1
    new_task = {"id": new_id, "title": data.get("title"), "done": False}
    tasks.append(new_task)
    return new_task

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return {"error": "Not found"}  # Still returns HTTP 200 OK!
```

### 📋 Version 3 Notes
1. **What changed in prompt:** Listed all required paths (`/`, `/health`, `/tasks`, `/tasks/{id}`) and specified HTTP methods for full CRUD.
2. **What improved in output:** All 5 CRUD doors were generated with proper path parameters (`task_id: int`) and payload extraction from JSON body.
3. **What still failed:** Errors return HTTP status 200 OK with `{"error": "Not found"}` instead of proper HTTP 404 status code, and `DELETE` returns a JSON string instead of standard HTTP 204 No Content.
4. **What to try next:** Add explicit HTTP status code constraints and input validation rules.

---

## 5. Version 4: Adding Layer 4 — Constraints & Status Code Criteria

### 🔵 Prompt v4 (Layer Added: Constraints & HTTP Status Code Rules)
> *"Write backend code for a todo app using Python and FastAPI on port 8000. Keep data in memory. Implement endpoints: GET /, GET /health, GET /tasks, GET /tasks/{id}, POST /tasks, PUT /tasks/{id}, and DELETE /tasks/{id}. CONSTRAINTS: Return HTTP 201 Created for POST, HTTP 204 No Content for DELETE, HTTP 404 Not Found if an ID doesn't exist (with JSON body {"error": "Task {id} not found"}), and HTTP 400 Bad Request if POST/PUT body has a missing or empty title string."*

### 📄 Representative Output Excerpt
```python
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(data: dict):
    if not data or "title" not in data or not str(data["title"]).strip():
        return JSONResponse(status_code=400, content={"error": "Title is required"})
    new_id = max([t["id"] for t in tasks], default=0) + 1
    new_task = {"id": new_id, "title": data["title"].strip(), "done": False}
    tasks.append(new_task)
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
```

### 📋 Version 4 Notes
1. **What changed in prompt:** Enforced HTTP status code mapping (201, 204, 400, 404) and input validation checks for empty strings.
2. **What improved in output:** The server now enforces REST compliance: correct 201/204 status codes, explicit 400 Bad Request validation, and custom JSON 404 errors.
3. **What still failed:** The generated file lacked inline OpenAPI docstrings for Swagger UI, query filtering parameters (`?done=true`, `?search=term`), and guidance on how a user should run or verify the server.
4. **What to try next:** Add verification requirements, Swagger documentation specs, and execution instructions.

---

## 6. Version 5: Adding Layer 5 — Verification & Reusability Specs

### 🔵 Prompt v5 (Layer Added: Verification Instructions & Reusability Specifications)
> *"Build a single-file Python FastAPI REST API for a task list running on port 8000. Storage must be in-memory (list of dicts with id, title, done). Implement GET /, GET /health, GET /tasks (supporting ?done=bool and ?search=str query filters), GET /tasks/{id}, POST /tasks, PUT /tasks/{id}, DELETE /tasks/{id}, GET /stats, and POST /reset. Enforce status codes: 200 for reads/updates, 201 Created for POST, 204 No Content for DELETE, 404 Not Found for invalid IDs, and 400 Bad Request for missing/empty titles. Add docstrings for OpenAPI Swagger UI at /docs. Include a verification script using TestClient or curl commands to test every status code."*

### 📄 Representative Output Excerpt
```python
# Complete single-file runnable solution with FastAPI, Swagger UI descriptions, 
# Pydantic schema validation, query parameters, stats, reset endpoints, 
# and automated TestClient verification suite.
```

### 📋 Version 5 Notes
1. **What changed in prompt:** Added OpenAPI documentation requirements, extra query parameters (`done`, `search`), helper endpoints (`/stats`, `/reset`), and self-contained execution/testing verification.
2. **What improved in output:** Produced a production-ready, zero-ambiguity single-file implementation with full Swagger UI documentation at `/docs` and runnable test scripts verifying every status code.
3. **What still failed:** Nothing failed. The output met all backend architectural, REST status code, and documentation requirements.
4. **What to try next:** Finalize into a reusable template prompt for any developer or AI assistant on the track.

---

## 🏆 Final Reusable Prompt (Engineered Spec)

> **Role & Task:** You are a senior backend engineer. Build a single-file Python FastAPI application implementing a complete Task CRUD REST API on `localhost:8000`.
>
> **Data Model & In-Memory Storage:**  
> Use an in-memory Python list initialized with 3 seed tasks (`id: int`, `title: str`, `done: bool`). Do not use any external database.
>
> **Required Endpoints & Status Codes:**  
> 1. `GET /` — Return `{"name": "Task API", "version": "1.0", "endpoints": [...]}` with HTTP 200.  
> 2. `GET /health` — Return `{"status": "ok"}` with HTTP 200.  
> 3. `GET /stats` — Return `{"total": int, "done": int, "open": int}` with HTTP 200.  
> 4. `POST /reset` — Reset database to initial 3 seed tasks with HTTP 200.  
> 5. `GET /tasks` — Return task list. Support optional query parameters: `done: bool` (filter by status) and `search: str` (filter by title substring).  
> 6. `GET /tasks/{id}` — Return task object with HTTP 200, or `{"error": "Task {id} not found"}` with HTTP 404.  
> 7. `POST /tasks` — Read JSON payload `{"title": "..."}`. Require title to be non-empty string (return HTTP 400 `{"error": "Title is required"}` if invalid). Auto-increment `id`, set `done=False`, append, and return task with HTTP 201 Created.  
> 8. `PUT /tasks/{id}` — Update `title` and/or `done`. Validate title if present (HTTP 400 if empty). Return updated task with HTTP 200, or HTTP 404 if ID missing.  
> 9. `DELETE /tasks/{id}` — Remove task and return empty body with HTTP 204 No Content, or HTTP 404 if ID missing.  
>
> **Documentation & Quality:**  
> Add clear summary and description tags to every endpoint route so Swagger UI at `/docs` is rich and interactive. Include a single-line command to run the server (`uvicorn main:app --reload --port 8000`).
