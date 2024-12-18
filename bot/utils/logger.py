import logging
import os

def setup_logger(name):
    """Sets up a logger with both file and console handlers
    
    Args:
        name (str): The name of the logger and its log file
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # File handler setup
        file_handler = logging.FileHandler(f'logs/{name}.log')
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        
        # Console handler setup
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger 