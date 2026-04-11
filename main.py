import imaplib
import os
from dotenv import load_dotenv
import email

from cleaning import decode_subject, clean_email_body, save_attachments
from storage import init_database, save_email, is_email_processed
from gmail_client import GmailClient
from categorizer import categorize

from logger import get_logger  
from priority_scorer import calculate_priority_score


logger = get_logger(__name__)

load_dotenv()
init_database()

EMAIL = os.getenv('EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')
IMAP_SERVER = os.getenv('IMAP_SERVER')

gmail = GmailClient(EMAIL, APP_PASSWORD, IMAP_SERVER)
gmail.connect()
gmail.connection.select('inbox')

status, message_ids = gmail.connection.search(None, 'UNSEEN')
logger.info(f"Unread count: {len(message_ids[0].split())}")

read_count = gmail.count_read_emails()
logger.info(f"Read emails in inbox: {read_count}")

labels = ['EmailAgent/SECURITY', 'EmailAgent/PROMOTION', 'EmailAgent/PERSONAL', 
            'EmailAgent/BUSINESS', 'EmailAgent/OTHER', 'EmailAgent/SOCIAL']

logger.info("\n--- Label Counts ---")
for label in labels:
    count = gmail.count_emails_in_label(label)
    logger.info(f"{label}: {count} emails")

for email_id_bytes in message_ids[0].split():
    email_id = email_id_bytes.decode()

    if is_email_processed(email_id):
        logger.info(f"Skipping {email_id} - already processed, but marking as read")
        gmail.mark_as_read(email_id_bytes)
        continue

    status, message_data = gmail.connection.fetch(email_id_bytes, '(RFC822)')
    logger.info(f"Processing email_id: {email_id}")
    
    if not message_data or not message_data[0]:
        logger.warning(f"Email {email_id} has no data, marking as read and skipping")
        gmail.mark_as_read(email_id_bytes)
        continue
    
    if message_data[0][1] is None:
        logger.warning(f"Email {email_id} has empty content, marking as read and skipping")
        gmail.mark_as_read(email_id_bytes)
        continue
    
    try:
        raw_email_string = message_data[0][1].decode('utf-8')
        email_message = email.message_from_bytes(raw_email_string.encode('utf-8'))
    except (UnicodeDecodeError, AttributeError) as e:
        logger.error(f"Failed to decode email {email_id}: {e}")
        gmail.mark_as_read(email_id_bytes)
        continue
    
    subject = email_message['Subject']
    sender = email_message['From']
    body = clean_email_body(email_message)
    category = categorize(subject, sender, body)
   
    saved_files = save_attachments(email_message, email_id, sender=sender)
    if saved_files:
        logger.info(f"Saved {len(saved_files)} attachment(s): {saved_files}")
    
    # CALCULATE PRIORITY SCORE 
    has_attachments = len(saved_files) > 0
    priority_score = calculate_priority_score(subject, sender, body, has_attachments)
    logger.info(f"Priority Score: {priority_score}/100")
    
    logger.info(f"Subject: {decode_subject(subject)}")
    
    logger.info(f"Subject: {decode_subject(subject)}")
    logger.info(f"Sender: {sender}")
    logger.info(f"Category: {category}")
    logger.info(f"Body preview: {body[:200]}")
    
    save_email(email_id, sender, subject, body)
    gmail.mark_as_read(email_id_bytes)
    gmail.move_to_label(email_id_bytes, f'EmailAgent/{category}')
    logger.info(f"Saved, marked, and moved to {category}\n")

gmail.disconnect()