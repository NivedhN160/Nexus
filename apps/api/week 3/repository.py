import os
import sqlite3
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod

class TaskRepository(ABC):
    @abstractmethod
    def get_all(self, done: Optional[bool] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def create(self, title: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update(self, task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, int]:
        pass

    @abstractmethod
    def reset(self) -> List[Dict[str, Any]]:
        pass


class PostgresTaskRepository(TaskRepository):
    def __init__(self, db_url: str):
        import psycopg2
        from psycopg2.extras import RealDictCursor
        self.db_url = db_url
        self.psycopg2 = psycopg2
        self.RealDictCursor = RealDictCursor

    def _get_conn(self):
        return self.psycopg2.connect(self.db_url, cursor_factory=self.RealDictCursor)

    def init_db(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_title ON tasks(title);")
        cursor.execute("SELECT COUNT(*) as count FROM tasks;")
        count = cursor.fetchone()["count"]
        if count == 0:
            initial_tasks = [
                ("Setup development environment", True),
                ("Watch request-response lecture", True),
                ("Build CRUD API for Week 2", False)
            ]
            for title, done in initial_tasks:
                cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s);", (title, done))
            conn.commit()
        conn.close()

    def get_all(self, done: Optional[bool] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        query = "SELECT id, title, done FROM tasks WHERE 1=1"
        params = []
        if done is not None:
            query += " AND done = %s"
            params.append(done)
        if search:
            query += " AND title ILIKE %s"
            params.append(f"%{search.strip()}%")
        query += " ORDER BY id ASC;"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r["id"], "title": r["title"], "done": bool(r["done"])} for r in rows]

    def get_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}

    def create(self, title: str) -> Dict[str, Any]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, FALSE) RETURNING id, title, done;", (title.strip(),))
        row = cursor.fetchone()
        conn.commit()
        conn.close()
        return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}

    def update(self, task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> Optional[Dict[str, Any]]:
        target = self.get_by_id(task_id)
        if not target:
            return None
        new_title = title.strip() if title is not None else target["title"]
        new_done = done if done is not None else target["done"]

        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET title = %s, done = %s WHERE id = %s;", (new_title, new_done, task_id))
        conn.commit()
        conn.close()
        return {"id": task_id, "title": new_title, "done": new_done}

    def delete(self, task_id: int) -> bool:
        if not self.get_by_id(task_id):
            return False
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
        conn.commit()
        conn.close()
        return True

    def get_stats(self) -> Dict[str, int]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM tasks;")
        total = cursor.fetchone()["total"]
        cursor.execute("SELECT COUNT(*) as done FROM tasks WHERE done = TRUE;")
        done_count = cursor.fetchone()["done"]
        conn.close()
        return {"total": total, "done": done_count, "open": total - done_count}

    def reset(self) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE tasks RESTART IDENTITY;")
        initial_tasks = [
            ("Setup development environment", True),
            ("Watch request-response lecture", True),
            ("Build CRUD API for Week 2", False)
        ]
        for title, done in initial_tasks:
            cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s);", (title, done))
        conn.commit()
        conn.close()
        return self.get_all()


class SQLiteTaskRepository(TaskRepository):
    def __init__(self, db_file: str = "tasks.db"):
        self.db_file = db_file

    def _get_conn(self):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_title ON tasks(title);")
        cursor.execute("SELECT COUNT(*) FROM tasks;")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO tasks (title, done) VALUES (?, ?);", [
                ("Setup development environment", True),
                ("Watch request-response lecture", True),
                ("Build CRUD API for Week 2", False)
            ])
            conn.commit()
        conn.close()

    def get_all(self, done: Optional[bool] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        query = "SELECT id, title, done FROM tasks WHERE 1=1"
        params = []
        if done is not None:
            query += " AND done = ?"
            params.append(1 if done else 0)
        if search:
            query += " AND title LIKE ?"
            params.append(f"%{search.strip()}%")
        query += " ORDER BY id ASC;"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r["id"], "title": r["title"], "done": bool(r["done"])} for r in rows]

    def get_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?;", (task_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}

    def create(self, title: str) -> Dict[str, Any]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, 0);", (title.strip(),))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return {"id": new_id, "title": title.strip(), "done": False}

    def update(self, task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> Optional[Dict[str, Any]]:
        target = self.get_by_id(task_id)
        if not target:
            return None
        new_title = title.strip() if title is not None else target["title"]
        new_done = done if done is not None else target["done"]

        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?;", (new_title, 1 if new_done else 0, task_id))
        conn.commit()
        conn.close()
        return {"id": task_id, "title": new_title, "done": new_done}

    def delete(self, task_id: int) -> bool:
        if not self.get_by_id(task_id):
            return False
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
        conn.commit()
        conn.close()
        return True

    def get_stats(self) -> Dict[str, int]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tasks;")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 1;")
        done_count = cursor.fetchone()[0]
        conn.close()
        return {"total": total, "done": done_count, "open": total - done_count}

    def reset(self) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks;")
        cursor.executemany("INSERT INTO tasks (title, done) VALUES (?, ?);", [
            ("Setup development environment", True),
            ("Watch request-response lecture", True),
            ("Build CRUD API for Week 2", False)
        ])
        conn.commit()
        conn.close()
        return self.get_all()


def get_repository() -> TaskRepository:
    db_url = os.getenv("DATABASE_URL", "")
    if db_url.startswith("postgresql://") or db_url.startswith("postgres://"):
        try:
            repo = PostgresTaskRepository(db_url)
            repo.init_db()
            print("Connected to PostgreSQL Repository!")
            return repo
        except Exception as e:
            print(f"PostgreSQL connection failed ({e}); falling back to SQLite repository.")
            
    repo = SQLiteTaskRepository("tasks.db")
    repo.init_db()
    print("Using SQLite Repository.")
    return repo
