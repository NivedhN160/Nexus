# Portfolio Case Study: General AI Fluency (Week 2)

## 📇 Voice Card
> **"Direct, plain-spoken, practical, honest, zero buzzwords."**

---

## 👤 Bio & Contact / CTA

### Bio
I'm a software developer building clean, high-performance backends and practical web tools. I focus on writing clear code, shipping tested APIs, and understanding how data flows from request to response without unnecessary complexity.

### Contact / Call to Action
Want to collaborate on backend systems or web projects? Reach out to me directly on GitHub at [github.com/NivedhN160](https://github.com/NivedhN160) or drop me an email to talk code.

---

## 📁 Case Study: Task CRUD API (W2 · A1)

### 1. The Problem
College coursework and backend projects often jump straight to complex databases and frameworks without explaining how HTTP request-response cycles actually work under the hood. I needed to build a lean, reliable REST API from scratch to master the core CRUD operations—creating, reading, updating, and deleting resources—and document every step with clear status codes and interactive documentation.

### 2. What I Did & Key Decisions
* **Selected FastAPI over Express:** Chose Python with FastAPI because it provides automated OpenAPI schema generation and built-in interactive Swagger UI (`/docs`), allowing instant API testing without extra boilerplate.
* **Embraced In-Memory Data Storage:** Deliberately kept state in a Python memory structure instead of attaching a database. This highlighted the "Mortality Experiment"—proving why non-volatile storage is necessary when server processes restart.
* **Strict Validation Rules:** Built explicit input validation handlers (`400 Bad Request`) to reject missing or empty titles before processing, enforcing the rule that a backend server must never trust incoming client payloads.
* **Atomic Stage Commits:** Maintained an authentic Git commit history across all development stages (from `hello server` to `full CRUD` and `AI rematch`), ensuring every single checkpoint was independently runnable.

### 3. What Came of It
* **Fully Operational API:** Delivered 9 verified REST endpoints handling full CRUD actions, query filtering (`?done=true`), keyword search (`?search=milk`), database resetting (`POST /reset`), and runtime statistics (`GET /stats`).
* **100% Test Coverage:** Verified all success (200, 201, 204) and error status codes (400, 404) via custom `TestClient` scripts and `curl -i` output logs.
* **Published Codebase:** Published a clean, production-ready repository at [github.com/NivedhN160/flyrank-w2-crud-api](https://github.com/NivedhN160/flyrank-w2-crud-api) complete with interactive Swagger UI docs.

---

## 🔄 Before / After Comparison

### Generic AI Copy (Before)
> *"Leveraged cutting-edge FastAPI architecture to architect a highly scalable, results-driven CRUD backend infrastructure, seamlessly optimizing endpoint throughput and maximizing developer efficiency."*

### Edited Version (After)
> *"I built a simple, 100-line FastAPI backend to master HTTP requests, status codes, and CRUD operations, testing every endpoint with curl and documenting it live in Swagger UI."*
