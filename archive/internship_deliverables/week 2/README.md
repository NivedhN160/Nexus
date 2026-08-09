# W2 · A1 — Task CRUD API (FlyRank AI Internship)

A complete, production-grade to-do list CRUD API built with Python 3.13 and FastAPI. This project demonstrates in-memory data management, RESTful status codes, input validation, automatic OpenAPI / Swagger UI interactive documentation, and clean Git commit history per assignment stage.

---

## 🚀 Quickstart: How to Run in Under 1 Minute

### Prerequisites
* Python 3.10+ installed on your system.

### One-Command Setup & Launch
```bash
python -m venv venv && source venv/bin/activate || venv\Scripts\activate && pip install -r requirements.txt && uvicorn main:app --reload --port 8000
```

Once running, visit:
* **Interactive API Docs (Swagger UI):** `http://localhost:8000/docs`
* **Root Endpoint:** `http://localhost:8000/`
* **Health Check:** `http://localhost:8000/health`

---

## 📋 Endpoints Summary

| HTTP Method | Path | Meaning / Description | Success Code | Error Codes |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Root API metadata & endpoints list | `200 OK` | - |
| `GET` | `/health` | Server health check | `200 OK` | - |
| `GET` | `/stats` | Task statistics (`total`, `done`, `open`) | `200 OK` | - |
| `POST` | `/reset` | Resets in-memory DB to 3 initial seed tasks | `200 OK` | - |
| `GET` | `/tasks` | List all tasks (supports `?done=true` & `?search=milk`) | `200 OK` | - |
| `GET` | `/tasks/{id}` | Retrieve details for a single task | `200 OK` | `404 Not Found` |
| `POST` | `/tasks` | Create a new task (requires non-empty `title`) | `201 Created` | `400 Bad Request` |
| `PUT` | `/tasks/{id}` | Update title and/or done status of a task | `200 OK` | `400 Bad Request`, `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Delete a task by ID | `204 No Content` | `404 Not Found` |

---

## 🧪 Sample `curl -i` Outputs

Below are authentic terminal `curl -i` outputs demonstrating status codes, headers, and responses for the full CRUD cycle:

### 1. Root Information (`GET /`)
```http
$ curl -i http://localhost:8000/
HTTP/1.1 200 OK
date: Tue, 04 Aug 2026 19:40:00 GMT
server: uvicorn
content-length: 83
content-type: application/json

{"name":"Task API","version":"1.0","endpoints":["/tasks","/health","/stats","/reset"]}
```

### 2. List All Tasks (`GET /tasks`)
```http
$ curl -i http://localhost:8000/tasks
HTTP/1.1 200 OK
date: Tue, 04 Aug 2026 19:40:00 GMT
server: uvicorn
content-length: 227
content-type: application/json

[
  {"id":1,"title":"Setup development environment","done":true},
  {"id":2,"title":"Watch request-response lecture","done":true},
  {"id":3,"title":"Build CRUD API for Week 2","done":false}
]
```

### 3. Retrieve Single Task (`GET /tasks/1`)
```http
$ curl -i http://localhost:8000/tasks/1
HTTP/1.1 200 OK
date: Tue, 04 Aug 2026 19:40:00 GMT
server: uvicorn
content-length: 60
content-type: application/json

{"id":1,"title":"Setup development environment","done":true}
```

### 4. 404 Error for Missing Task (`GET /tasks/99`)
```http
$ curl -i http://localhost:8000/tasks/99
HTTP/1.1 404 Not Found
date: Tue, 04 Aug 2026 19:40:00 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"error":"Task 99 not found"}
```

### 5. Create Task (`POST /tasks`)
```http
$ curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
HTTP/1.1 201 Created
date: Tue, 04 Aug 2026 19:40:00 GMT
server: uvicorn
content-length: 41
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

### 6. 400 Validation Error (`POST /tasks` with empty body)
```http
$ curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{}'
HTTP/1.1 400 Bad Request
date: Tue, 04 Aug 2026 19:40:00 GMT
server: uvicorn
content-length: 28
content-type: application/json

{"error":"Title is required"}
```

### 7. Update Task (`PUT /tasks/4`)
```http
$ curl -i -X PUT http://localhost:8000/tasks/4 -H "Content-Type: application/json" -d '{"done":true}'
HTTP/1.1 200 OK
date: Tue, 04 Aug 2026 19:40:00 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":4,"title":"Buy milk","done":true}
```

### 8. Delete Task (`DELETE /tasks/4`)
```http
$ curl -i -X DELETE http://localhost:8000/tasks/4
HTTP/1.1 204 No Content
date: Tue, 04 Aug 2026 19:40:00 GMT
server: uvicorn
```

---

## 🎨 Interactive Swagger UI Documentation

FastAPI generates automatic, interactive OpenAPI documentation served at `http://localhost:8000/docs`.

### Features in Swagger UI:
* **Interactive Endpoints:** Expand any route (`GET`, `POST`, `PUT`, `DELETE`).
* **Try it Out:** Test requests directly inside the browser without needing curl.
* **Schema Validation:** Displays request schemas (`TaskCreateSchema`, `TaskUpdateSchema`) and expected HTTP response codes.

---

## 🧪 The Mortality Experiment

### What Happens When You Restart the Server?
1. Create new tasks (e.g. task `#4` and `#5`) using `POST /tasks`.
2. Confirm they exist using `GET /tasks`.
3. Stop the Uvicorn server (`Ctrl+C`) and start it again.
4. Run `GET /tasks`.

### Observation & Explanation
When the server restarts, all newly added or modified tasks disappear, and the database resets to the original 3 seed tasks (`tasks_db`). 

**Why?**
The task list is stored strictly **in-memory** in RAM (`tasks_db` python list variable). RAM is volatile memory—when the process terminates, the operating system reclaims memory, erasing state. Persistent databases (SQL/NoSQL) exist specifically to solve this problem by saving state to non-volatile disk storage.

---

## 🥊 Stage 7: The AI Rematch ("AI vs Me")

### The Prompt Used
> *"Build a lightweight RESTful CRUD API for managing a to-do list in Python using FastAPI. Create an in-memory list with 3 initial seed tasks (`id`, `title`, `done`). Include `GET /`, `GET /health`, `GET /tasks`, `GET /tasks/{id}`, `POST /tasks`, `PUT /tasks/{id}`, and `DELETE /tasks/{id}`. Ensure `POST` returns status 201 Created and validates non-empty title with 400 Bad Request. Ensure `DELETE` returns 204 No Content. Return 404 for missing IDs as `{"error": "..."}`. Provide Swagger UI at `/docs`."*

### Analysis & Diff Answers

#### 1. What did the AI do better — and do you understand its version well enough to explain it?
* **Pydantic Validation:** The AI used Pydantic's `BaseModel` with `min_length=1` and `Field(...)` for automated payload parsing rather than raw dictionary/JSON inspection. This cleanly handles type coercion and automatic OpenAPI documentation for request bodies.

#### 2. What did it get wrong or quietly ignore from your prompt?
* **Error Response Format:** The AI used `raise HTTPException(status_code=404, detail="...")` which outputs `{"detail": "..."}` instead of the exact requested custom JSON schema `{"error": "..."}`.
* **Input Validation Details:** When empty or missing JSON bodies were posted, FastAPI returned a default `422 Unprocessable Entity` validation error instead of the explicitly requested `400 Bad Request`.

#### 3. What did your prompt forget to specify — and what did the AI silently decide for you?
* **Validation Status Code:** The prompt asked for `400 Bad Request` on invalid input, but didn't specify how Pydantic's default 422 validation handler should be overridden. The AI silently defaulted to FastAPI's built-in 422 response.
* **Auto-increment Logic:** The prompt specified assigning the next ID, and the AI decided to calculate `max(id) + 1` dynamically.

#### Prompt Iteration Result
Updating the prompt to explicitly specify `@app.exception_handler(RequestValidationError)` and custom response models produced a 100% match with custom status codes and JSON error schemas.

---

## 📌 Commit Log History

```text
* Stage 7: AI vs me
* Stage 6: publish and docs
* Extras: query filtering, stats, reset, and search
* Stage 5: Swagger UI
* Stage 4: full CRUD
* Stage 3: create with validation
* Stage 2: read endpoints with 404
* Stage 1: root and health endpoints
* Stage 0: hello server
```
