

from logger import get_logger

logger = get_logger(__name__)

def calculate_priority_score(subject, sender, body):
    """
    Calculate priority score for an email
    
    Args:
        subject: Email subject line
        sender: Email sender address
        body: Email body text
    
    Returns:
        int: Score from 0 to 100
    """
    logger.debug(f"Calculating priority score for: {sender}")
    
    score = 50
    
    full_text = f"{subject} {body}".lower()
    
    urgency_keywords = ['urgent', 'asap', 'immediate', 
                        'action required', 'time sensitive',
                        'important', 'priority', 'deadline',
                        'emergency', 'attention', 'critical', 
                        'invoice', 'payment', 'meeting', 'schedule',
                        'follow up', 'response needed' ]
    if any(word in full_text for word in urgency_keywords):
        score += 30
        logger.debug(f"  +30: Urgency keywords found")
    
    return min(score, 100)