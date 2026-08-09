-- Database Initialization Script for Postgres in Docker
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stretch Goal Index: Accelerate search queries on task title
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
