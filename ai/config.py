import os
from dotenv import load_dotenv

load_dotenv()

class AIConfig:
    """Central configuration for AI features"""
    
    # Groq API settings
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
    
    # Feature flags
    ENABLE_AI_CATEGORIZER = True
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'groq')
    
    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY:
            print("WARNING: GROQ_API_KEY not found in .env file")
            return False
        print(f"AI Configuration valid. Using Groq model: {cls.GROQ_MODEL}")
        return True

ai_config = AIConfig()