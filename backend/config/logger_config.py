import logging


class Logger:
    def __init__(self, name: str = "logger", level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Define log format
        log_format = logging.Formatter(
            "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)d] %(levelname)s: %(message)s"
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        self.logger.addHandler(console_handler)

    def init_logger(self):
        return self.logger


logger = Logger(name="backend_logger").init_logger()
