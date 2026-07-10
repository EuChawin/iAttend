import sqlite3
import os
from . import config

def get_connection() -> sqlite3.Connection:
    """
    Returns a connection to the SQLite database.
    Creates the database file if it doesn't exist.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(config.DB_PATH), exist_ok=True)
    return sqlite3.connect(config.DB_PATH)

def ensure_tables() -> None:
    """
    Ensures that the necessary tables exist in the database.
    """
    conn = get_connection()
    c = conn.cursor()
    
    # Students table
    c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT UNIQUE,
        student_id TEXT UNIQUE,
        name TEXT
    )
    ''')
    
    # Daily attendance table
    c.execute('''
    CREATE TABLE IF NOT EXISTS attendance_daily (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        date TEXT,
        entry_time TEXT,
        exit_time TEXT,
        late INTEGER DEFAULT 0,
        attended INTEGER DEFAULT 0,
        UNIQUE(student_id, date)
    )
    ''')
    
    conn.commit()
    conn.close()

# Initialize tables automatically when this module is imported
ensure_tables()
