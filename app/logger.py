import logging


def setup_logger(level=logging.DEBUG):
    logger = logging.getLogger("app_logger")
    logger.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(console_handler)
    return logger


app_logger = setup_logger()
