from ai.categorizer import GroqCategorizer
from ai.logger import ai_logger

class AIService:
    """Unified service for all AI operations"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        ai_logger.info("Starting AI Service with Groq...")
        self.categorizer = GroqCategorizer()
        ai_logger.info("AI Service ready")
    
    def categorize_email(self, subject, sender, body):
        """Categorize a single email"""
        return self.categorizer.categorize(subject, sender, body)
    
    def get_status(self):
        """Get AI service status"""
        return {
            'categorizer_available': self.categorizer.is_available(),
            'provider': 'groq',
            'model': self.categorizer.model if hasattr(self.categorizer, 'model') else 'unknown'
        }

ai_service = AIService()