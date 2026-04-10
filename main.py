import imaplib
import os
from dotenv import load_dotenv

print("Step 1: Loading environment variables...")
load_dotenv()

EMAIL = os.getenv('EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')
IMAP_SERVER = os.getenv('IMAP_SERVER')

print(f"Step 2: Email: {EMAIL}")
print(f"Step 3: IMAP Server: {IMAP_SERVER}")
print(f"Step 4: Password loaded (length: {len(APP_PASSWORD) if APP_PASSWORD else 0})")

print("Step 5: Attempting to connect...")
mail = imaplib.IMAP4_SSL(IMAP_SERVER)

print("Step 6: Connected! Attempting login...")
mail.login(EMAIL, APP_PASSWORD)

print("Step 7: Login successful!")

mail.logout()
print("Step 8: Done!")