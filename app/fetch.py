#!/usr/bin/env python
"""
Fetch emails for a specific email account from the database
Usage: python fetch.py <account_id>
"""

import sys
import sqlite3
import imaplib
import email
from email.header import decode_header
from datetime import datetime

DB_NAME = "emails.db"

def get_account(account_id):
    """Get account credentials from database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, email, app_password_encrypted, imap_server 
        FROM email_accounts 
        WHERE id = ?
    ''', (account_id,))
    account = cursor.fetchone()
    conn.close()
    return account

def clean_body(email_message):
    """Extract plain text from email body"""
    body = ""
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                    break
                except:
                    pass
    else:
        try:
            body = email_message.get_payload(decode=True).decode('utf-8', errors='replace')
        except:
            body = "Could not decode body"
    return body[:500]

def fetch_emails(account_id, email_address, app_password, imap_server):
    """Fetch unread emails from Gmail"""
    
    print(f"📧 Connecting to {email_address}...")
    
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, app_password)
        mail.select('inbox')
        print(f"✅ Connected successfully")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return 0
    
    status, message_ids = mail.search(None, 'UNSEEN')
    
    if status != 'OK' or not message_ids[0]:
        print("📭 No new emails found")
        mail.logout()
        return 0
    
    email_ids = message_ids[0].split()
    print(f"📬 Found {len(email_ids)} unread emails")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    new_count = 0
    duplicate_count = 0
    error_count = 0
    
    for e_id in email_ids:
        status, msg_data = mail.fetch(e_id, '(RFC822)')
        
        if status != 'OK' or not msg_data[0]:
            error_count += 1
            continue
        
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # Get subject
        subject = msg['Subject']
        if subject:
            try:
                decoded = decode_header(subject)[0]
                if isinstance(decoded[0], bytes):
                    subject = decoded[0].decode(decoded[1] or 'utf-8', errors='replace')
                else:
                    subject = decoded[0]
            except:
                subject = "Could not decode subject"
        else:
            subject = "No Subject"
        
        sender = msg['From'] or "Unknown"
        body = clean_body(msg)
        
        # Use INSERT OR IGNORE to skip duplicates
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO processed_emails (account_id, email_id, sender, subject, body_preview, processed_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (account_id, e_id.decode(), sender, subject, body, datetime.now()))
            
            if cursor.rowcount > 0:
                new_count += 1
                if new_count <= 10:
                    print(f"  ✅ Saved: {subject[:50]}...")
            else:
                duplicate_count += 1
        except Exception as e:
            error_count += 1
            print(f"  ❌ Error: {e}")
    
    conn.commit()
    conn.close()
    mail.logout()
    
    print(f"\n{'='*50}")
    print(f"📊 SUMMARY for {email_address}")
    print(f"{'='*50}")
    print(f"   ✅ New emails saved: {new_count}")
    print(f"   ⏭️  Duplicates skipped: {duplicate_count}")
    print(f"   ❌ Errors: {error_count}")
    
    return new_count

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fetch.py <account_id>")
        sys.exit(1)
    
    account_id = int(sys.argv[1])
    
    account = get_account(account_id)
    
    if not account:
        print(f"❌ Account ID {account_id} not found")
        sys.exit(1)
    
    print(f"📡 Fetching emails for account ID: {account_id}")
    fetch_emails(account[0], account[1], account[2], account[3])