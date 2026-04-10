import sqlite3
from datetime import datetime

DB_NAME = "emails.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_emails (
            email_id TEXT PRIMARY KEY,
            sender TEXT,
            subject TEXT,
            body_preview TEXT,
            processed_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_email(email_id, sender, subject, body_preview):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO processed_emails (email_id, sender, subject, body_preview, processed_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (email_id, sender, subject, body_preview[:200], datetime.now()))
    conn.commit()
    conn.close()

def is_email_processed(email_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM processed_emails WHERE email_id = ?', (email_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None