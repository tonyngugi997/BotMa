import imaplib

class GmailClient:
    def __init__(self, email, app_password, imap_server="imap.gmail.com"):
        self.email = email
        self.app_password = app_password
        self.imap_server = imap_server
        self.connection = None
    
    def connect(self):
        self.connection = imaplib.IMAP4_SSL(self.imap_server)
        self.connection.login(self.email, self.app_password)
        return self.connection
    
    def disconnect(self):
        if self.connection:
            self.connection.logout()
    
    def mark_as_read(self, email_id):
        self.connection.store(email_id, '+FLAGS', '\\Seen')