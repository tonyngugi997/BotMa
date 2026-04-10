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
    """Extract plain text from email, aggressively clean HTML garbage"""
    
    body_text = ""
    
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body_bytes = part.get_payload(decode=True)
                body_text = body_bytes.decode('utf-8', errors='replace')
                break
            elif part.get_content_type() == "text/html":
                body_bytes = part.get_payload(decode=True)
                body_text = body_bytes.decode('utf-8', errors='replace')
    else:
        body_bytes = email_message.get_payload(decode=True)
        body_text = body_bytes.decode('utf-8', errors='replace')
    
    if not body_text:
        return "No body found"
    

    #html cleaning
    import re
    
    body_text = re.sub(r'<style[^>]*>.*?</style>', ' ', body_text, flags=re.DOTALL)
    
    body_text = re.sub(r'<script[^>]*>.*?</script>', ' ', body_text, flags=re.DOTALL)
    
    body_text = re.sub(r'<!--.*?-->', ' ', body_text, flags=re.DOTALL)
    
    body_text = re.sub(r'<table[^>]*>', ' ', body_text)
    body_text = re.sub(r'</table>', ' ', body_text)
    body_text = re.sub(r'<tr[^>]*>', ' ', body_text)
    body_text = re.sub(r'</tr>', ' ', body_text)
    body_text = re.sub(r'<td[^>]*>', ' ', body_text)
    body_text = re.sub(r'</td>', ' ', body_text)
    
    body_text = re.sub(r'<[^>]+>', ' ', body_text)
    
    import html
    body_text = html.unescape(body_text)
    
    lines = body_text.split('\n')
    cleaned_lines = []
    for line in lines:
        if not line.strip().startswith('>'):
            cleaned_lines.append(line)
    body_text = '\n'.join(cleaned_lines)
    
    signature_markers = ['-- ', '---', 'Sent from my', 'Best regards', 'Cheers,', 'Thanks,']
    for marker in signature_markers:
        if marker in body_text:
            body_text = body_text.split(marker)[0]
    
    # Clean up whitespace
    body_text = re.sub(r'\n\s*\n', '\n\n', body_text)  # Multiple newlines to double
    body_text = re.sub(r'[ \t]+', ' ', body_text)       # Multiple spaces/tabs to single space
    body_text = re.sub(r'\n[ \t]+', '\n', body_text)    # Spaces after newline
    body_text = re.sub(r'^\s+', '', body_text, flags=re.MULTILINE)  # Leading spaces on lines
    body_text = re.sub(r'\s+$', '', body_text, flags=re.MULTILINE)  # Trailing spaces on lines
    body_text = re.sub(r'\n{3,}', '\n\n', body_text)    # More than 2 newlines down to 2
    
    return body_text.strip()

def save_attachments(email_message, email_id, save_folder="attachments"):
    """Save all attachments from an email to disk"""
    import os
    
    saved_files = []
    
    if not email_message.is_multipart():
        return saved_files
    
    for part in email_message.walk():
        content_disposition = str(part.get("Content-Disposition"))
        
        if "attachment" not in content_disposition:
            continue
        
        filename = part.get_filename()
        if filename:
            # Decode filename if encoded
            from email.header import decode_header
            decoded_filename = decode_header(filename)[0][0]
            if isinstance(decoded_filename, bytes):
                filename = decoded_filename.decode('utf-8', errors='replace')
            else:
                filename = decoded_filename
            
            # Clean filename 
            import re
            filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
            
            # Full path
            filepath = os.path.join(save_folder, f"{email_id}_{filename}")
            
            # Save the file
            with open(filepath, 'wb') as f:
                f.write(part.get_payload(decode=True))
            
            saved_files.append(filepath)
    
    return saved_files