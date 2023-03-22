import logging.handlers

_LOG_FILE: str = 'inlife.log'
_LOG_MAX_BYTES: int = 1024 * 1024 * 10
_BACKUP_COUNT: int = 5

log_handler = logging.handlers.RotatingFileHandler(
  filename=_LOG_FILE,
  maxBytes=_LOG_MAX_BYTES,
  backupCount=_BACKUP_COUNT
)

log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)
