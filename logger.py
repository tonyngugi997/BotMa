# logger.py
import logging
import os

def setup_logger():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Created {log_dir} folder")
    
    logging.basicConfig(
        level=logging.DEBUG,  
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/email_agent.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logger()

logger.debug("This is DEBUG - for detailed troubleshooting")
logger.info("This is INFO - for normal operations")
logger.warning("This is WARNING - for something unexpected but not broken")
logger.error("This is ERROR - for something that failed")
logger.critical("This is CRITICAL - for catastrophic failures")