import os
import logging
from watchtower import CloudWatchLogHandler

env = os.environ


def get_logger(log_output, cloudwatch_group, cloudwatch_stream, log_level):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    if log_output == "cloudwatch":
        handler = CloudWatchLogHandler(
            log_group=cloudwatch_group, stream_name=cloudwatch_stream
        )
        handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
        logger.addHandler(handler)
    else:
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger
