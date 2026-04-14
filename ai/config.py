 
import os
from dotenv import load_dotenv

load_dotenv()

class AIConfig:
    """Central configuration for AI features"""
    
    # Gemini API settings
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    
    ENABLE_AI_CATEGORIZER = True
    ENABLE_AI_PRIORITY = False  
    ENABLE_AI_SUMMARY = False     
    
    MAX_REQUESTS_PER_MINUTE = 15
    
    @classmethod
    def validate(cls):
        """Check if AI is properly configured"""
        if not cls.GEMINI_API_KEY:
            print("⚠️ GEMINI_API_KEY not found in .env file")
            return False
        print(f"✅ AI Configuration valid. Using model: {cls.GEMINI_MODEL}")
        return True

ai_config = AIConfig()