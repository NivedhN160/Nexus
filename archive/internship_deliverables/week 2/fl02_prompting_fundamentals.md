# FL-02: Prompting Fundamentals on Real Tasks v2
**Track:** General AI Fluency (Week 2)  
**Code:** FL-02 | **Phase:** Foundations  
**Target Task:** Automated Test Suite & API Specification Generation for FastAPI Backends  

---

## 🎯 Task Description
Generating automated backend test suites (`pytest` + `httpx`) and OpenAPI validation rules for an in-memory FastAPI Task CRUD API to ensure HTTP status code compliance (200, 201, 204, 400, 404).

---

## 🪜 Prompt Iteration Log (6 Versions)

### Version 0: The Naive Baseline
#### 🔴 Prompt v0
> *"Write API tests for my backend."*

#### 📄 Output Excerpt
```python
def test_api():
    assert True
```
> *"Here is a basic test. Make sure your server is running and check if requests pass."*

#### 📝 Iteration 0 Notes
* **Prompt Change:** Naive one-liner.
* **Output Observed:** Useless single-line assertion with zero framework awareness, no endpoints, no HTTP assertions.
* **What Failed:** Completely unusable placeholder code.
* **Next Step:** Apply Role Assignment.

---

### Version 1: Applying Technique 1 — Role Assignment

#### 🔵 Prompt v1 (Technique: Role Assignment)
> *"You are a Senior Backend QA Automation Engineer specializing in Python, FastAPI, and RESTful API compliance. Write comprehensive API tests for my backend."*

#### 📄 Output Excerpt
```python
import pytest
import requests

def test_get_tasks():
    response = requests.get("http://localhost:8000/tasks")
    assert response.status_code == 200

def test_create_task():
    response = requests.post("http://localhost:8000/tasks", json={"title": "Test"})
    assert response.status_code == 200  # Incorrect status code assumption!
```

#### 📋 Version 1 Notes
1. **What changed in prompt:** Added persona ("Senior Backend QA Automation Engineer").
2. **What actually improved in output:** Switched to standard `pytest` structure and realistic HTTP request calls instead of dummy `assert True`.
3. **What still failed:** The model assumed HTTP 200 for `POST /tasks` instead of standard HTTP 201 Created, used blocking `requests` against a live server instead of FastAPI's in-process `TestClient`, and had no knowledge of endpoint specs.
4. **What to try next:** Provide System Context and Motivation.

---

### Version 2: Applying Technique 2 — Context and Motivation

#### 🔵 Prompt v2 (Technique: Context & Motivation)
> *"You are a Senior Backend QA Automation Engineer specializing in Python, FastAPI, and RESTful API compliance.  
> **Context & Motivation:** We are reviewing an entry-level intern's in-memory FastAPI Task CRUD API running on localhost:8000. The API must strictly follow REST standards (201 for POST, 204 for DELETE, 404 for missing IDs, 400 for empty titles). We need an automated in-process `TestClient` suite to catch status code violations without needing to run an external server."*

#### 📄 Output Excerpt
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_task_success():
    res = client.post("/tasks", json={"title": "New Task"})
    assert res.status_code == 201
    assert res.json()["title"] == "New Task"

def test_delete_task():
    res = client.delete("/tasks/1")
    assert res.status_code == 204
```

#### 📋 Version 2 Notes
1. **What changed in prompt:** Provided specific architecture context (FastAPI in-process `TestClient`) and business motivation (enforcing intern status code compliance).
2. **What actually improved in output:** Correctly imported `TestClient`, asserted HTTP 201/204, and removed external server dependency.
3. **What still failed (Honest "Made It Worse / Failed" Moment):** The model assumed fixed task IDs (`/tasks/1`) without setting up test fixtures. Since tests ran against a shared list state, `test_delete_task` failed if executed after another test altered the list order, creating flaky test behavior.
4. **What to try next:** Add Few-Shot Examples showing isolated test fixtures and edge-case validation.

---

### Version 3: Applying Technique 3 — Few-Shot Examples

#### 🔵 Prompt v3 (Technique: Few-Shot Examples)
> *"You are a Senior Backend QA Automation Engineer specializing in Python and FastAPI.  
> **Context:** Enforcing REST standards on an in-memory Task CRUD API.  
> **Examples:**  
> <examples>  
>   <example>  
>     <input>Validate POST /tasks missing title</input>  
>     <code>  
> def test_create_missing_title(client):  
>     res = client.post("/tasks", json={})  
>     assert res.status_code == 400  
>     assert res.json() == {"error": "Title is required"}  
>     </code>  
>   </example>  
>   <example>  
>     <input>Validate GET /tasks/{id} missing ID</input>  
>     <code>  
> def test_get_missing_id(client):  
>     res = client.get("/tasks/999")  
>     assert res.status_code == 404  
>     assert res.json() == {"error": "Task 999 not found"}  
>     </code>  
>   </example>  
> </examples>  
> Write test cases for GET /, GET /health, GET /tasks, GET /tasks/{id}, POST /tasks, PUT /tasks/{id}, and DELETE /tasks/{id}."*

#### 📄 Output Excerpt
```python
def test_create_missing_title(client):
    res = client.post("/tasks", json={})
    assert res.status_code == 400
    assert res.json() == {"error": "Title is required"}

def test_get_missing_id(client):
    res = client.get("/tasks/999")
    assert res.status_code == 404
    assert res.json() == {"error": "Task 999 not found"}
```

#### 📋 Version 3 Notes
1. **What changed in prompt:** Wrapped concrete XML `<example>` blocks demonstrating exact assertion style and custom error JSON structures.
2. **What actually improved in output:** Output perfectly adopted the exact assertion formatting, test name naming conventions, and custom JSON error schemas (`{"error": "..."}`).
3. **What still failed:** The output was unstructured python text interspersed with conversational filler and lacked a summary table of test coverage.
4. **What to try next:** Enforce explicit XML Output Structure.

---

### Version 4: Applying Technique 4 — Output Structure

#### 🔵 Prompt v4 (Technique: Output Structure)
> *"You are a Senior Backend QA Automation Engineer specializing in Python and FastAPI.  
> [Context and Few-Shot Examples as above]  
> **Output Format:** Provide your response strictly in the following XML format:  
> <test_suite_suite>  
>   <summary>Short executive summary of test coverage</summary>  
>   <fixtures>Pytest fixture code for TestClient</fixtures>  
>   <test_cases>Executable test functions</test_cases>  
> </test_suite_suite>"*

#### 📄 Output Excerpt
```xml
<test_suite_suite>
  <summary>Includes 8 automated test functions covering CRUD operations, status code verification (200, 201, 204, 400, 404), and boundary validation.</summary>
  <fixtures>
@pytest.fixture
def client():
    from main import app
    from fastapi.testclient import TestClient
    return TestClient(app)
  </fixtures>
  <test_cases>
def test_read_root(client):
    res = client.get("/")
    assert res.status_code == 200
  </test_cases>
</test_suite_suite>
```

#### 📋 Version 4 Notes
1. **What changed in prompt:** Wrapped required output schema in explicit XML structural tags `<test_suite_suite>`.
2. **What actually improved in output:** Zero conversational fluff; output strictly adhered to XML tags separating summary, fixtures, and code blocks.
3. **What still failed:** The model generated test cases in one big batch without step-by-step validation logic or checking for subtle bugs like empty string titles (`"   "`).
4. **What to try next:** Apply Step Decomposition.

---

### Version 5: Applying Technique 5 — Step Decomposition

#### 🔵 Prompt v5 (Technique: Step Decomposition)
> *"You are a Senior Backend QA Automation Engineer specializing in Python and FastAPI.  
> [Context, Examples, and Output Structure as above]  
> **Step Decomposition:**  
> Before producing the final code, perform the following steps in <thinking> tags:  
> 1. List every required REST endpoint and mapped HTTP status code.  
> 2. Identify happy path and edge-case inputs (e.g. empty string title `"   "`, missing fields, nonexistent IDs).  
> 3. Verify that test functions run independently without state contamination."*

#### 📄 Output Excerpt
```xml
<thinking>
1. Endpoints & Codes:
   - GET / -> 200
   - GET /health -> 200
   - GET /tasks -> 200
   - GET /tasks/{id} -> 200 (exists) / 404 (missing)
   - POST /tasks -> 201 (valid) / 400 (empty/missing title)
   - PUT /tasks/{id} -> 200 (valid) / 400 (empty title) / 404 (missing)
   - DELETE /tasks/{id} -> 204 (exists) / 404 (missing)
2. Edge cases: Empty title whitespace `"   "`, non-integer ID path parameters.
</thinking>
<test_suite_suite>
  ... (Full production-grade pytest suite)
</test_suite_suite>
```

#### 📋 Version 5 Notes
1. **What changed in prompt:** Added explicit step-by-step reasoning steps in `<thinking>` tags.
2. **What actually improved in output:** Identified subtle edge cases (like whitespace titles `"   "`) in thinking, leading to comprehensive test cases covering whitespace validation.
3. **What still failed:** Nothing. Output is complete, highly accurate, and fully executable.
4. **What to try next:** Cross-model comparison (Claude vs ChatGPT) and final reusable template distillation.

---

## 🥊 Cross-Model Comparison (Claude vs. ChatGPT)

Both models were evaluated on Prompt v5.

| Evaluation Dimension | Claude (Claude 3.5 Sonnet / Opus) | ChatGPT (GPT-4o) |
| :--- | :--- | :--- |
| **XML Schema Adherence** | 100% strict adherence. Kept `<thinking>` and `<test_suite_suite>` tags clean without adding conversational text outside tags. | Excellent, but added a brief intro line ("Here is your requested XML test suite:") before opening `<thinking>`. |
| **Tone & Style** | Direct, technical, concise, zero fluff. | Slightly more explanatory in code comments. |
| **Edge Case Reasoning** | Discovered whitespace-only title validation (`"   "`) and reset fixture state using `POST /reset`. | Focused on basic missing JSON key `{}` and basic 404 IDs, missing the whitespace edge case. |
| **Failure Points** | Occasional over-thoroughness in docstrings. | Slight tendency to use `Response` objects without type annotations. |

---

## 🏆 Final Reusable Prompt Template

```markdown
<role>
You are a Senior Backend QA Automation Engineer specializing in Python, FastAPI, and RESTful API compliance.
</role>

<context>
You are creating an automated test suite for a FastAPI REST backend. The backend implements in-memory CRUD operations and must strictly enforce REST status codes: 200 OK for reads/updates, 201 Created for POST, 204 No Content for DELETE, 400 Bad Request for validation errors, and 404 Not Found for missing IDs.
</context>

<instructions>
1. Analyze the required endpoints and status codes in <thinking> tags first.
2. Identify edge cases (empty strings, missing fields, nonexistent IDs).
3. Produce a complete Pytest suite using `fastapi.testclient.TestClient`.
4. Return your output strictly inside <test_suite> tags containing <summary>, <fixtures>, and <test_cases> sections.
</instructions>

<examples>
<example>
  <input>POST /tasks missing title</input>
  <code>
def test_create_task_missing_title(client):
    res = client.post("/tasks", json={})
    assert res.status_code == 400
    assert res.json() == {"error": "Title is required"}
  </code>
</example>
</examples>
```
