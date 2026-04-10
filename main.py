import imaplib
import os
from dotenv import load_dotenv
import email

from cleaning import decode_subject, clean_email_body, save_attachments
from storage import init_database, save_email, is_email_processed
from gmail_client import GmailClient
from categorizer import categorize

load_dotenv()
init_database()

EMAIL = os.getenv('EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')
IMAP_SERVER = os.getenv('IMAP_SERVER')

gmail = GmailClient(EMAIL, APP_PASSWORD, IMAP_SERVER)
gmail.connect()
gmail.connection.select('inbox')

status, message_ids = gmail.connection.search(None, 'UNSEEN')
print(f"Unread count: {len(message_ids[0].split())}")

for email_id_bytes in message_ids[0].split():
    email_id = email_id_bytes.decode()
    
    if is_email_processed(email_id):
        print(f"Skipping {email_id} - already processed")
        continue
    
    status, message_data = gmail.connection.fetch(email_id_bytes, '(RFC822)')
    print(f"Processing email_id: {email_id}")
    
    raw_email_string = message_data[0][1].decode('utf-8')
    email_message = email.message_from_bytes(raw_email_string.encode('utf-8'))
    
    subject = email_message['Subject']
    sender = email_message['From']
    body = clean_email_body(email_message)
    category = categorize(subject, sender, body)
    saved_files = save_attachments(email_message, email_id)
    if saved_files:
        print(f"Saved {len(saved_files)} attachment(s): {saved_files}")
    
    print(f"Subject: {decode_subject(subject)}")
    print(f"Sender: {sender}")
    print(f"Category: {category}")
    print(f"Body preview: {body[:200]}")
    
    save_email(email_id, sender, subject, body)
    gmail.mark_as_read(email_id_bytes)
    gmail.move_to_label(email_id_bytes, f'EmailAgent/{category}')
    print(f"Saved, marked, and moved to {category}\n")

gmail.disconnect()