import logging
from datetime import datetime
import os

class AILogger:
    """Specialized logger for AI operations to track usage and errors"""
    
    def __init__(self):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        
        self.logger = logging.getLogger('ai_module')
        self.logger.setLevel(logging.INFO)
        
        # Avoid duplicate handlers
        if not self.logger.handlers:
            log_file = f"logs/ai_{datetime.now().strftime('%Y-%m-%d')}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            ))
            self.logger.addHandler(file_handler)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(
                '%(asctime)s - 🔍 AI: %(message)s'
            ))
            self.logger.addHandler(console_handler)
    
    def info(self, msg):
        self.logger.info(msg)
    
    def error(self, msg):
        self.logger.error(msg)
    
    def warning(self, msg):
        self.logger.warning(msg)
    
    def debug(self, msg):
        self.logger.debug(msg)

ai_logger = AILogger()