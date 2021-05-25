import logging


def Main():
    logger = logging.getLogger("DJFry")

    formatter = logging.Formatter('%(asctime)s | %(levelname)s - (%(message)s):%(module)s')

    console_logs = logging.StreamHandler()
    console_logs.setLevel(logging.INFO)
    console_logs.setFormatter(formatter)
    file_logs = logging.FileHandler("DJFry_Log.txt")
    file_logs.setLevel(logging.DEBUG)
    file_logs.setFormatter(formatter)

    logger.addHandler(console_logs)
    logger.addHandler(file_logs)
    logger.setLevel(logging.DEBUG)
    return logger
