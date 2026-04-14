import sqlite3
from datetime import datetime

conn = sqlite3.connect('emails.db')
cur = conn.cursor()

# Try to insert a test email with account_id=3
cur.execute('''
    INSERT OR IGNORE INTO processed_emails (account_id, email_id, sender, subject, body_preview, processed_at)
    VALUES (?, ?, ?, ?, ?, ?)
''', (3, 'TEST_ACCOUNT_3', 'test@example.com', 'Test for Account 3', 'This is a test body', datetime.now()))

conn.commit()
print(f"Rows inserted: {cur.rowcount}")
conn.close()

# Verify it worked
conn = sqlite3.connect('emails.db')
count = conn.execute('SELECT COUNT(*) FROM processed_emails WHERE account_id = 3').fetchone()[0]
print(f"Account 3 now has {count} emails")

# Show the test email
email = conn.execute('SELECT email_id, subject, account_id FROM processed_emails WHERE account_id = 3').fetchone()
if email:
    print(f"Test email: {email}")
conn.close()