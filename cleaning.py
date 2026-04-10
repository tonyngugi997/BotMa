from email.header import decode_header

def decode_subject(subject):
    if subject is None:
        return ""
    decoded_parts = decode_header(subject)
    decoded_string = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            decoded_string += part.decode(encoding or 'utf-8', errors='replace')
        else:
            decoded_string += str(part)
    return decoded_string


def clean_email_body(email_message):
    """Extract plain text from email, remove HTML"""
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body_bytes = part.get_payload(decode=True)
                return body_bytes.decode('utf-8', errors='replace')
        
        for part in email_message.walk():
            if part.get_content_type() == "text/html":
                body_bytes = part.get_payload(decode=True)
                body_text = body_bytes.decode('utf-8', errors='replace')
                body_text = body_text.replace('<br>', '\n')
                import re
                body_text = re.sub(r'<[^>]+>', '', body_text)
                return body_text
    else:
        body_bytes = email_message.get_payload(decode=True)
        return body_bytes.decode('utf-8', errors='replace')
    
    return "No body found"