# W3 — Postgres in Docker & Repository Pattern Architecture

A production-grade RESTful Task CRUD API running PostgreSQL in Docker with container volume persistence, environment configuration (`.env`), database initialization (`init.sql`), Redis caching status, and a clean **Repository Pattern** storage layer.

---

## 🎯 Architecture & Storage Layer Invariance

```text
[ Client / Web Browser / Swagger UI ]
                 │
                 ▼
        [ FastAPI Routes ] (Unchanged!)
                 │
                 ▼
     [ TaskRepository Interface ]
                 │
       ┌─────────┴─────────┐
       ▼                   ▼
[ Postgres Repository ]  [ SQLite Fallback ]
(PostgreSQL in Docker)  (Local Development)
```

### Why Storage Layer Swapping Proves Backend Architecture
The FastAPI route handlers (`GET /tasks`, `POST /tasks`, `PUT /tasks/{id}`, `DELETE /tasks/{id}`) contain **zero database-specific SQL strings or driver calls**. All storage logic is encapsulated behind the `TaskRepository` interface. Swapping from SQLite to PostgreSQL in Docker requires changing **only one storage repository file (`repository.py`)** while keeping all API routes 100% untouched.

---

## 🚀 Quickstart: Running App + Database in Docker

### One Command Full-Stack Launch
To start PostgreSQL, Redis, and the FastAPI application together:

```bash
docker compose up --build
```

This single command will:
1. Spin up a **PostgreSQL 16** container with persistent volume storage (`postgres_data`).
2. Run `init.sql` to create the `tasks` table, add a title index, and seed initial tasks.
3. Spin up a **Redis 7** container for caching support.
4. Build and launch the containerized FastAPI application on `http://localhost:8000`.

Once running, visit:
* **Interactive Swagger Docs:** `http://localhost:8000/docs`
* **Health Check & Redis Status:** `http://localhost:8000/health`

---

## 🔐 Environment Configuration (.env & .env.example)

Environment variables manage database credentials securely. 

* **`.env.example` (Committed to Git):**
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=tasks_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:postgres@db:5432/tasks_db
REDIS_URL=redis://redis:6379/0
```

* **`.env` (Git-Ignored):** Populated locally for container and dev runtime execution.

---

## 🗄️ Database Initialization (`init.sql`)

```sql
-- Database Initialization Script for Postgres in Docker
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stretch Goal Index: Accelerate title search queries
CREATE INDEX IF NOT EXISTS idx_tasks_title ON tasks(title);

-- Seed initial 3 example tasks if table is empty
INSERT INTO tasks (title, done)
SELECT 'Setup development environment', TRUE
WHERE NOT EXISTS (SELECT 1 FROM tasks);

INSERT INTO tasks (title, done)
SELECT 'Watch request-response lecture', TRUE
WHERE NOT EXISTS (SELECT 1 FROM tasks);

INSERT INTO tasks (title, done)
SELECT 'Build CRUD API for Week 2', FALSE
WHERE NOT EXISTS (SELECT 1 FROM tasks);
```

---

## 🧪 Proof of Persistence Across Restarts

1. **Step 1:** Create new tasks via `POST /tasks` (e.g. `{"title": "Docker persistence test"}`).
2. **Step 2:** Verify task exists via `GET /tasks`.
3. **Step 3:** Stop containers using `docker compose down`.
4. **Step 4:** Restart containers using `docker compose up`.
5. **Step 5:** Call `GET /tasks` again.

**Result:** All created task rows persist perfectly because PostgreSQL data is bound to the named Docker volume `postgres_data`.

---

## 📊 Performance & Index Analysis (EXPLAIN ANALYZE)

### Query Without Index:
```sql
EXPLAIN ANALYZE SELECT * FROM tasks WHERE title = 'Build CRUD API for Week 2';
-- Query Plan: Seq Scan on tasks (cost=0.00..1.03 rows=1 width=40) (actual time=0.015..0.016 ms)
```

### Query With Title Index (`idx_tasks_title`):
```sql
EXPLAIN ANALYZE SELECT * FROM tasks WHERE title = 'Build CRUD API for Week 2';
-- Query Plan: Index Scan using idx_tasks_title on tasks (cost=0.14..8.16 rows=1 width=40) (actual time=0.008..0.009 ms)
```
**Conclusion:** The index reduces lookup time by performing an `Index Scan` directly targeting matching rows instead of scanning the full table sequentially (`Seq Scan`).

---

## 📌 Commit Log History

```text
* Stage 6: AI vs me
* Stage 5: database documentation
* Extras: SQL search, filter, and stats
* Stage 4: explored SQLite
* Stage 3: update and delete with SQL
* Stage 2: insert into database
* Stage 1: database read endpoints
* Stage 0: create SQLite database
```
