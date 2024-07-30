import logging
import uuid
import sys


def unique_logger(name: str = None):
    if not name:
        request_uid = uuid.uuid1().hex[:8]
    else:
        request_uid = f"{name}-{uuid.uuid1().hex[:4]}"

    logger = logging.getLogger(f"{request_uid}")

    # Create a file handler
    file_handler = logging.FileHandler("log.log")

    # Create a stream handler to print to console
    stream_handler = logging.StreamHandler(sys.stdout)

    # Create a formatter and set the format for the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

    # Log some messages
    return logger
