from loguru import logger
from config.settings import settings
import sys

def setup_logger():
    logger.remove()
    logger.add(sys.stdout, level=settings.log_level, format="<green>{time}</green> | <level>{level}</level> | <cyan>{name}</cyan> | {message}")
    return logger

logger = setup_logger()