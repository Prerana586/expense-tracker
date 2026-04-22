import sqlite3
from pathlib import Path

DB = Path("expenses.db")

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                amount      REAL NOT NULL,
                currency    TEXT DEFAULT 'USD',
                category    TEXT,
                description TEXT,
                date        TEXT
            )
        """)

def save_expense(expense: dict):
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "INSERT INTO expenses (amount, currency, category, description, date) "
            "VALUES (?, ?, ?, ?, ?)",
            (expense["amount"], expense.get("currency", "USD"),
             expense["category"], expense["description"], expense["date"])
        )

def fetch_all() -> list:
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM expenses ORDER BY date DESC"
        ).fetchall()
    return [dict(r) for r in rows]