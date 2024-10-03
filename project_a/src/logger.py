import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('NetworkApp')
logger.setLevel(logging.DEBUG)

# File handler
file_handler = RotatingFileHandler('logs/network_app.log', maxBytes=100000, backupCount=10)
file_handler.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)