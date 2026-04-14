import google.generativeai as genai
from ai.config import ai_config
from ai.logger import ai_logger

class AICategorizer:
    """AI-powered email categorizer using Google Gemini"""
    
    def __init__(self):
        """Initialize Gemini client"""
        ai_logger.info("Initializing AI Categorizer...")
        
        if not ai_config.validate():
            ai_logger.error("AI not configured properly. Check your GEMINI_API_KEY")
            self.available = False
            return
        
        # Configure Gemini
        genai.configure(api_key=ai_config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(ai_config.GEMINI_MODEL)
        self.available = True
        
        ai_logger.info(f"✅ AI Categorizer ready with model: {ai_config.GEMINI_MODEL}")
    
    def is_available(self):
        """Check if AI is ready to use"""
        return self.available

if __name__ == "__main__":
    print("Testing AI Categorizer initialization...")
    categorizer = AICategorizer()
    print(f"Available: {categorizer.is_available()}")