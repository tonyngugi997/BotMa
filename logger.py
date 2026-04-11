# logger.py
import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

# Create the logger instance
logger = setup_logger()

logger.info("Logger is working!")