import sqlite3

DB_NAME = "emails.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_emails (
            email_id TEXT PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()


def save_email(email_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO processed_emails (email_id) VALUES (?)', (email_id,))
    conn.commit()
    conn.close()