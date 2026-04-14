import sys
import sqlite3
import imaplib
import email
from email.header import decode_header
from datetime import datetime

DB_NAME = "emails.db"

def get_account(account_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, app_password_encrypted, imap_server FROM email_accounts WHERE id = ?', (account_id,))
    account = cursor.fetchone()
    conn.close()
    return account

def fetch_emails(account_id, email_addr, password, server):
    print(f"Fetching for account_id={account_id}: {email_addr}")
    
    try:
        mail = imaplib.IMAP4_SSL(server)
        mail.login(email_addr, password)
        mail.select('inbox')
        print("Connected!")
    except Exception as e:
        print(f"Connection failed: {e}")
        return
    
    status, ids = mail.search(None, 'ALL')
    if status != 'OK' or not ids[0]:
        print("No emails found")
        mail.logout()
        return
    
    email_ids = ids[0].split()
    print(f"Found {len(email_ids)} emails")
    
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    new_count = 0
    
    for eid in email_ids[:100]:  # Limit to 100 for testing
        status, data = mail.fetch(eid, '(RFC822)')
        if status != 'OK' or not data[0]:
            continue
        
        msg = email.message_from_bytes(data[0][1])
        subject = msg['Subject'] or "No Subject"
        sender = msg['From'] or "Unknown"
        
        # Get body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='replace')[:500]
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='replace')[:500]
        
        # Save with account_id
        cur.execute('''
            INSERT OR IGNORE INTO processed_emails (account_id, email_id, sender, subject, body_preview, processed_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (account_id, eid.decode(), sender, subject, body, datetime.now()))
        
        if cur.rowcount > 0:
            new_count += 1
            print(f"  Saved: {subject[:40]}")
    
    conn.commit()
    conn.close()
    mail.logout()
    
    print(f"\nDone! Saved {new_count} new emails for account_id={account_id}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fetch2.py <account_id>")
        sys.exit(1)
    
    account_id = int(sys.argv[1])
    acc = get_account(account_id)
    
    if not acc:
        print(f"Account {account_id} not found")
        sys.exit(1)
    
    fetch_emails(acc[0], acc[1], acc[2], acc[3])