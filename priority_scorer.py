

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
    
    return score