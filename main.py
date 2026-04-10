import imaplib
import os
from dotenv import load_dotenv
import email

from cleaning import decode_subject, clean_email_body
from storage import init_database, save_email, is_email_processed


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

# Loop through each unread email
for email_id_bytes in message_ids[0].split():
    email_id = email_id_bytes.decode()
    
    # Skip if already processed
    if is_email_processed(email_id):
        print(f"Skipping {email_id} - already processed")
        continue
    
    # Fetch the email
    status, message_data = mail.fetch(email_id_bytes, '(RFC822)')
    print(f"Processing email_id: {email_id}")
    
    # Parse email
    raw_email_string = message_data[0][1].decode('utf-8')
    email_message = email.message_from_bytes(raw_email_string.encode('utf-8'))
    
    # Extract fields
    subject = email_message['Subject']
    sender = email_message['From']
    body = clean_email_body(email_message)
    
    # Display
    print(f"Subject: {decode_subject(subject)}")
    print(f"Sender: {sender}")
    print(f"Body preview: {body[:200]}")
    
    # Save to db
    save_email(email_id, sender, subject, body)
    print(f"Saved {email_id} to database\n")

mail.logout()