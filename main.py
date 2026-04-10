import imaplib
import os
from re import I
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv('EMAIL' )
APP_PASSWORD = os.getenv('APP_PASSWORD')
IMAP_SERVER = os.getenv('IMAP_SERVER')

mail = imaplib.IMAP4_SSL(IMAP_SERVER)

mail.login(EMAIL, APP_PASSWORD)

mail.logout()