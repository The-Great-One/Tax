import sqlite3
from pathlib import Path

DB_PATH = Path('tally.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        type TEXT
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS ledger (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        account_id INTEGER,
        debit REAL DEFAULT 0,
        credit REAL DEFAULT 0,
        description TEXT,
        FOREIGN KEY(account_id) REFERENCES accounts(id)
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        quantity REAL DEFAULT 0,
        rate REAL DEFAULT 0
    )
    ''')
    conn.commit()
    conn.close()


def delete_transaction(entry_id: int) -> None:
    """Remove a ledger entry by its primary key."""
    conn = get_connection()
    conn.execute("DELETE FROM ledger WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
