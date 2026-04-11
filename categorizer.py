def categorize(subject, sender, body):
    text = f"{subject} {sender} {body}".lower()
    
    if any(word in text for word in ['security', 'alert', 'verification', 'password', 'reset']):
        return "SECURITY"
    
    if any(word in text for word in ['newsletter', 'unsubscribe', 'promo', 'sale', 'deal']):
        return "PROMOTION"
    
    if any(word in text for word in ['invoice', 'receipt', 'order', 'purchase', 'payment']):
        return "BUSINESS"
    
    if any(word in sender.lower() for word in ['gmail', 'yahoo', 'outlook']):
        return "PERSONAL"
    
    if any(word in sender.lower() for word in ['reddit', 'twitter', 'facebook', 'instagram', 'linkedin', 'tiktok', 'discord', 'telegram']):
        return "SOCIAL"
    
    return "OTHER"