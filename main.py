import imaplib
import os
from dotenv import load_dotenv

print("Loading environment variables...")
load_dotenv()

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
print(f"email_id: {first_id.decode()} - Status: {status}")

mail.logout()
