import logging

def get_api_logger(logger_name, log_level=logging.DEBUG):
    """GET app loggers"""

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    log_format = "> %(asctime)s - %(filename)s - %(lineno)d - %(message)s"
    log_formatter = logging.Formatter(log_format)
    request_handler = logging.StreamHandler()
    request_handler.setFormatter(log_formatter)
    logger.addHandler(request_handler)
    return logger

error_logger = get_api_logger(logger_name="error", log_level=logging.ERROR)
app_logger = get_api_logger(logger_name="app", log_level=logging.INFO)

