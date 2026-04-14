import os
from groq import Groq
from ai.config import ai_config
from ai.logger import ai_logger

class GroqCategorizer:
    """AI-powered email categorizer using Groq (faster & higher free limits)"""
    
    def __init__(self):
        """Initialize Groq client"""
        ai_logger.info("Initializing Groq Categorizer...")
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            ai_logger.error("GROQ_API_KEY not found. Please add to .env file")
            self.available = False
            return
        
        # Initialize Groq client
        self.client = Groq(api_key=api_key)
        self.model = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
        self.available = True
        
        ai_logger.info(f"Groq Categorizer ready with model: {self.model}")
    
    def is_available(self):
        """Check if AI is ready to use"""
        return self.available
    
    def categorize(self, subject, sender, body):
        """
        Categorize email using Groq's ultra-fast inference
        """
        if not self.available:
            ai_logger.warning("Groq not available, falling back to rule-based")
            return self._fallback_categorize(subject, sender, body)
        
        truncated_body = body[:1000] if body else ""
        
        system_prompt = """You are an email classification system. 
Classify emails into EXACTLY ONE category: SECURITY, BUSINESS, PERSONAL, PROMOTION, SOCIAL, or OTHER.
Reply with ONLY the category name, nothing else."""

        user_prompt = f"""
Email details:
From: {sender}
Subject: {subject}
Body: {truncated_body}

Category (choose one: SECURITY, BUSINESS, PERSONAL, PROMOTION, SOCIAL, OTHER):
"""
        
        try:
            ai_logger.info(f"Categorizing email from {sender[:30]}...")
            
            # Groq API call - super fast!
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Low temp for consistent categories
                max_tokens=20,     # We only need one word
                top_p=1
            )
            
            category = response.choices[0].message.content.strip().upper()
            
            valid_categories = ['SECURITY', 'BUSINESS', 'PERSONAL', 'PROMOTION', 'SOCIAL', 'OTHER']
            if category in valid_categories:
                ai_logger.info(f"Groq Category: {category}")
                return category
            else:
                ai_logger.warning(f"Unexpected response: {category}, defaulting to OTHER")
                return 'OTHER'
                
        except Exception as e:
            ai_logger.error(f"Groq categorization failed: {e}")
            return self._fallback_categorize(subject, sender, body)
    
    def _fallback_categorize(self, subject, sender, body):
        """Fallback to rule-based categorization if AI fails"""
        text = f"{subject} {sender} {body}".lower()
        
        if any(word in text for word in ['security', 'alert', 'verification', 'password', 'reset', '2fa', 'mfa']):
            return "SECURITY"
        if any(word in text for word in ['newsletter', 'unsubscribe', 'promo', 'sale', 'deal', 'coupon', 'marketing']):
            return "PROMOTION"
        if any(word in text for word in ['invoice', 'receipt', 'order', 'purchase', 'payment', 'bill', 'subscription']):
            return "BUSINESS"
        if any(word in sender.lower() for word in ['gmail', 'yahoo', 'outlook', 'icloud', 'proton']):
            return "PERSONAL"
        if any(word in sender.lower() for word in ['reddit', 'twitter', 'x.com', 'facebook', 'instagram', 'linkedin', 'tiktok']):
            return "SOCIAL"
        return "OTHER"

# Quick test when run directly
if __name__ == "__main__":
    print("\nTesting Groq Categorizer...")
    categorizer = GroqCategorizer()
    
    if categorizer.is_available():
        test_cases = [
            ("Your account login alert", "security@bank.com", "New login detected from Chrome", "SECURITY"),
            ("Weekly Newsletter", "news@techcrunch.com", "Here are top stories", "PROMOTION"),
            ("Dinner plans", "mom@gmail.com", "What time should we meet?", "PERSONAL"),
            ("Invoice #123", "billing@amazon.com", "Your payment of $49.99 is due", "BUSINESS"),
            ("Someone liked your tweet", "noreply@twitter.com", "Your post got a like", "SOCIAL"),
        ]
        
        print("\nRunning tests with Groq (fast inference)...")
        for subject, sender, body, expected in test_cases:
            result = categorizer.categorize(subject, sender, body)
            status = "PASS" if result == expected else "FAIL"
            print(f"{status} - Expected: {expected}, Got: {result}")
            print(f"  Subject: {subject}\n")
    else:
        print("Groq not available. Check your API key.")