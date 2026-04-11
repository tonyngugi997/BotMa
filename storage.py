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
            category TEXT,
            priority_score INTEGER DEFAULT 50,
            processed_at TIMESTAMP
        )
    ''')
    
    try:
        cursor.execute('ALTER TABLE processed_emails ADD COLUMN priority_score INTEGER DEFAULT 50')
        print("Added priority_score column")
    except sqlite3.OperationalError:
        pass  
    
    conn.commit()
    conn.close()

def save_email(email_id, sender, subject, body_preview, category, priority_score=50):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO processed_emails (email_id, sender, subject, body_preview, category, priority_score, processed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (email_id, sender, subject, body_preview[:200], category, priority_score, datetime.now()))
    conn.commit()
    conn.close()

def is_email_processed(email_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM processed_emails WHERE email_id = ?', (email_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None