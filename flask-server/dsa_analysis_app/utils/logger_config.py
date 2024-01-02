import logging

def setup_logger(name):
    """ Set up and return a logger with the specified name. """
    logger = logging.getLogger(name)
    FORMAT = '[%(asctime)s %(filename)s->%(funcName)s():%(lineno)d] %(levelname)s: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    return logger