

from logger import get_logger

logger = get_logger(__name__)

def calculate_priority_score(subject, sender, body, has_attachments=False):
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
    
    urgency_keywords = [
                            'urgent', 'asap', 'immediate', 
                            'action required', 'time sensitive',
                            'important', 'priority', 'deadline',
                            'emergency', 'attention', 'critical', 
                            'invoice', 'payment', 'meeting', 'schedule',
                            'follow up', 'response needed' 
                        ]
    if any(word in full_text for word in urgency_keywords):
        score += 30
        logger.debug(f"  +30: Urgency keywords found")
    
    security_keywords = [  
                            'security alert', 'login attempt', 
                            'password reset', 'verification code',
                            'suspicious activity',
                            'account compromised', 'unauthorized access',
                            'phishing', 'data breach', 'malware detected',
                            'security update', 'security notice', 'security warning',
                            'security incident', 'security breach', 'security issue',
                            'security concern', 'security risk', 'security vulnerability',
                            'security threat', 'security alert', 'security advisory',
                            'security bulletin', 'security notification', 'security report',
                            'security update', 'security patch', 'security fix',
                            'security enhancement', 'security improvement', 'security measure',
                            'security protocol', 'security policy', 'security procedure',
                            'security guideline', 'security best practice', 'security recommendation',
                            'security awareness', 'security training', 'security education',
                            'security awareness training'
                    ]
    if any(word in full_text for word in security_keywords):
        score += 40
        logger.debug(f"  +40: Security alert detected")

    if has_attachments:
        score += 10
        logger.debug(f"  +10: Email has attachments")


    promotion_keywords = [
                            'unsubscribe', 'promo', 'sale', 'deal',
                              'discount', 'coupon', 'newsletter',
                              'offer', 'promotion', 'advertisement', 'advertising',
                              'marketing', 'campaign', 'special offer',
                              'limited time', 'exclusive', 'clearance', 'bargain',
                              'free trial', 'gift', 'bonus', 'reward',
                              'loyalty program', 'membership', 'vip', 'early access',
                              'flash sale', 'daily deal', 'weekly deal', 'seasonal sale',
                              'holiday sale', 'black friday', 'cyber monday', 'boxing day',
                                'new arrival', 'product launch', 'event invitation',
                                'webinar', 'workshop', 'conference', 'trade show',
                                'giveaway', 'contest', 'sweepstakes', 'raffle',
                                'prize', 'win', 'winner', 'winning', 'claim your prize',
                                'enter to win', 'enter now', 'limited offer', 'act now',
                                'don\'t miss', 'last chance', 'final call', 'while supplies last',
                                'exclusive offer', 'vip access', 'members only', 'insider deal',
                                'secret sale', 'hidden deal', 'unadvertised offer', 'private sale',
                                'exclusive deal', 'exclusive promotion', 'exclusive discount'
                                
                        ]
    if any(word in full_text for word in promotion_keywords):
        score -= 20
        logger.debug(f"  -20: Promotion keywords detected")
    
    return min(score, 100)