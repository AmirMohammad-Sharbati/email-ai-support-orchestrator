from loguru import logger
import sys

def setup_logger():
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="<green>{time}</green> | <level>{level}</level> | <cyan>{name}</cyan> | {message}")
    return logger

logger = setup_logger()