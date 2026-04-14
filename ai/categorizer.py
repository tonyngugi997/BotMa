import os
from groq import Groq
from ai.config import ai_config
from ai.logger import ai_logger

class GroqCategorizer:
    """AI-powered email categorizer using Groq"""
    
    def __init__(self):
        """Initialize Groq client"""
        ai_logger.info("Initializing Groq Categorizer...")
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            ai_logger.error("GROQ_API_KEY not found. Please add to .env file")
            self.available = False
            return
        
        self.client = Groq(api_key=api_key)
        self.model = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
        self.available = True
        
        ai_logger.info(f"Groq Categorizer ready with model: {self.model}")
    
    def is_available(self):
        return self.available
    
    def categorize(self, subject, sender, body):
        """Categorize email using Groq AI - NO FALLBACK"""
        
        if not self.available:
            raise Exception("Groq AI not available - check API key")
        
        truncated_body = body[:1000] if body else ""
        
        system_prompt = """You are an email classification system. 
Classify emails into EXACTLY ONE category: SECURITY, BUSINESS, PERSONAL, PROMOTION, SOCIAL, or OTHER.
Reply with ONLY the category name, nothing else."""

        user_prompt = f"""
Email details:
From: {sender}
Subject: {subject}
Body: {truncated_body}

Category:
"""
        
        ai_logger.info(f"Categorizing email from {sender[:30]}...")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=20,
            top_p=1
        )
        
        category = response.choices[0].message.content.strip().upper()
        
        valid_categories = ['SECURITY', 'BUSINESS', 'PERSONAL', 'PROMOTION', 'SOCIAL', 'OTHER']
        if category in valid_categories:
            ai_logger.info(f"Groq Category: {category}")
            return category
        else:
            return 'OTHER'

# Test
if __name__ == "__main__":
    print("\nTesting Groq Categorizer...")
    c = GroqCategorizer()
    
    if c.is_available():
        result = c.categorize(
            "Your account login alert", 
            "security@bank.com", 
            "New login detected"
        )
        print(f"Result: {result}")