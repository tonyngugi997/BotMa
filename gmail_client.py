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
    



    def add_label(self, email_id, label_name):
        """Add a label to an email (Gmail uses '\\Label1' format)"""
        # Gmail requires label names to be in a specific format
        # For custom labels, you need the label's internal name
        self.connection.store(email_id, '+X-GM-LABELS', label_name)
    
    def move_to_label(self, email_id, label_name):
        """Move email to a label and remove from inbox"""
        # Add the label
        self.connection.store(email_id, '+X-GM-LABELS', label_name)
        # Remove from inbox
        self.connection.store(email_id, '+FLAGS', '\\Deleted')
        # Expunge removes deleted items
        self.connection.expunge()

    def disconnect(self):
        if self.connection:
            self.connection.logout()
    
    def mark_as_read(self, email_id):
        self.connection.store(email_id, '+FLAGS', '\\Seen')