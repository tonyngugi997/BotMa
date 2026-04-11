# logger.py
import logging
import os

def setup_logger():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Created {log_dir} folder")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/email_agent.log'),  
            logging.StreamHandler()                      
        ]
    )
    return logging.getLogger(__name__)

# Create the logger instance
logger = setup_logger()

logger.info("Logger is now writing to file!")