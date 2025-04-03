# functions/logging_config.py
import logging


def setup_logger(name):
    """Set up and return a logger, ensuring no duplicate handlers are added."""
    logger = logging.getLogger(name)
    logger.propagate = False  # Disable propagation to parent loggers
    # Check if the logger already has handlers to avoid adding multiple handlers
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)  # Set the logging level (DEBUG, INFO, etc.)

        # Create console handler and set level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Create formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        ch.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(ch)

    return logger
