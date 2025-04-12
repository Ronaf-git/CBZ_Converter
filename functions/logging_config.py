# functions/logging_config.py
import logging

# Create the logger object globally
logger = logging.getLogger('global_logger')

def setup_logger(name, log_file='app.log'):
    """Set up and return a logger, ensuring no duplicate handlers are added, 
    and output both to console and log file."""
    
    # Get a logger instance with the specified name
    logger = logging.getLogger(name)
    
    # Disable propagation to the root logger
    logger.propagate = False

    # Remove existing handlers (if any), to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set the logging level
    logger.setLevel(logging.DEBUG)  # Set the logging level (DEBUG, INFO, etc.)

    # Create console handler and set level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter and add it to the console handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(ch)

    # Create file handler (set mode to 'a' to append)
    fh = logging.FileHandler(log_file, mode='a')  # Open file in append mode
    fh.setLevel(logging.DEBUG)  # Ensure it writes debug level and higher to the file

    # Add the same formatter to the file handler
    fh.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(fh)

    return logger
