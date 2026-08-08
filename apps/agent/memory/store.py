import sqlite3
import os
from core.logger import setup_logger
logger = setup_logger(__name__)

import datetime

os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"

import logging
logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.CRITICAL)

import chromadb

MEMORY_DIR = os.path.dirname(__file__)
SQLITE_DB_PATH = os.path.join(MEMORY_DIR, "neos_memory.db")
CHROMA_DB_PATH = os.path.join(MEMORY_DIR, "chroma_db")

class MemoryStore:
    def __init__(self):
        self.conn = sqlite3.connect(SQLITE_DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                role TEXT,
                content TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE,
                value TEXT
            )
        ''')
        self.conn.commit()

        from chromadb.config import Settings
        self.chroma_client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.chroma_client.get_or_create_collection(name="neos_memory")

    def add_interaction(self, role, content):
        timestamp = datetime.datetime.now().isoformat()
        
        self.cursor.execute("INSERT INTO interactions (timestamp, role, content) VALUES (?, ?, ?)", 
                            (timestamp, role, content))
        self.conn.commit()
        
        doc_id = f"interaction_{timestamp}_{role}"
        try:
            self.collection.add(
                documents=[content],
                metadatas=[{"timestamp": timestamp, "role": role}],
                ids=[doc_id]
            )
        except Exception as e:
            logger.info(f"ChromaDB Error: {e}")

    def set_fact(self, key, value):
        self.cursor.execute("INSERT OR REPLACE INTO facts (key, value) VALUES (?, ?)", (key, value))
        self.conn.commit()

    def get_fact(self, key):
        self.cursor.execute("SELECT value FROM facts WHERE key = ?", (key,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_recent_context(self, limit=10):
        self.cursor.execute("SELECT role, content FROM interactions ORDER BY id DESC LIMIT ?", (limit,))
        rows = self.cursor.fetchall()
        return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

    def semantic_search(self, query, n_results=3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        if results['documents'] and results['documents'][0]:
            return results['documents'][0]
        return []

memory_store = MemoryStore()
