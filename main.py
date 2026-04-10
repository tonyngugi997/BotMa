import imaplib
import os
from dotenv import load_dotenv
import email

from cleaning import decode_subject, clean_email_body
from storage import init_database, save_email


print("Loading environment variables...")
load_dotenv()
init_database()


EMAIL = os.getenv('EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')
IMAP_SERVER = os.getenv('IMAP_SERVER')

print(" Attempting to connect...")
mail = imaplib.IMAP4_SSL(IMAP_SERVER)

print("Attempting login...")
mail.login(EMAIL, APP_PASSWORD)
print("Login successful!")

mail.select('inbox')

status, message_ids = mail.search(None, 'UNSEEN')
print(f"Unread count: {len(message_ids[0].split())}")

first_id = message_ids[0].split()[0]
status, message_data = mail.fetch(first_id, '(RFC822)')
print(f"email_id: {first_id.decode()} ")

raw_email_string = message_data[0][1].decode('utf-8')
email_message = email.message_from_bytes(raw_email_string.encode('utf-8'))
subject = email_message['Subject']
sender = email_message['From']
print(f"Subject: {decode_subject(subject)}")
save_email(first_id.decode())
print(f"Sender: {sender}")
body = clean_email_body(email_message)
print(f"Body preview: {body[:200]}")

mail.logout()
