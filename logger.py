import logging
import os
from datetime import datetime

def get_logger(name, log_file=None):
    """
    Create a logger with a specific name
    
    Args:
        name: The name of the logger (usually __name__)
        log_file: Optional specific log file name
    
    Returns:
        A configured logger object
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    if log_file is None:
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = f"logs/email_agent_{today}.log"
    else:
        log_file = f"logs/{log_file}"
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

if __name__ == "__main__":
    log = get_logger("test")
    log.debug("This goes to file only")
    log.info("This goes to file AND console")
    log.error("This also goes everywhere")