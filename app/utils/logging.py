import logging.handlers
from app.constant.core import LOG_FILE, LOG_MAX_BYTES, BACKUP_COUNT

log_handler = logging.handlers.RotatingFileHandler(
  filename=LOG_FILE,
  maxBytes=LOG_MAX_BYTES,
  backupCount=BACKUP_COUNT
)

log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)
