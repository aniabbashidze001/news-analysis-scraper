import logging

def setup_logger(name="news_scraper", log_file="project.log", level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger