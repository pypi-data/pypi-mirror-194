import logging


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(filename="scheduler/log/schedule.log")
    file_handler.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)

    # formatter = logging.Formatter("%(asctime)s - module:%(module)s -> %(funcName)s -  %(levelname)s - %(message)s")
    formatter = logging.Formatter("%(asctime)-16s   %(name)-20s -> %(funcName)-30s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M")
    console.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger


if __name__ == "__main__":
    pass