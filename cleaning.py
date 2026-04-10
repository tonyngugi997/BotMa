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