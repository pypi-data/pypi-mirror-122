# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import logging
import sys


# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------
default_log_format = '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
def get_logger(log_level=20, format=default_log_format, streams=[sys.stdout]):
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # remove any handlers so we only use our handler
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    
    log_handlers = []
    for stream in streams:
        log_handlers.append(logging.StreamHandler(stream))
    
    logging.basicConfig(
        level=log_level,
        format=format,
        handlers=log_handlers
    )

    return logger
