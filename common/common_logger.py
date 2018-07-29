import logging as lg

'''Create Logger.You can overwrite as you need.'''
def get_logger(name):
    logger = lg.getLogger(name)
    fmt = lg.Formatter("%(asctime)s[%(levelname)s][%(name)s]:%(message)s")
    logger.setLevel(lg.DEBUG)

    file_handler = lg.FileHandler('./log/' + name, 'a')
    file_handler.setLevel(lg.INFO)
    file_handler.setFormatter(fmt)

    file_handler_debug = lg.FileHandler('./log/' + name + '_debug', 'a')
    file_handler_debug.setLevel(lg.DEBUG)
    file_handler_debug.setFormatter(fmt)

    stream_handler = lg.StreamHandler()
    stream_handler.setLevel(lg.DEBUG)
    stream_handler.setFormatter(fmt)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.addHandler(file_handler_debug)
    return logger