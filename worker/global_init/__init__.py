from config import config
from .logger import Logger
from .celery import initialize_celery

app = initialize_celery()
logger = Logger(
    debug=config.LOGGER_DEBUG,
    identifier=config.LOGGER_IDENTIFIER,
    max_bytes=config.LOGGER_MAX_BYTE,
    backup_count=config.LOGGER_DEBUG
)

logger.info(f"Celery app started.")

from .dbsession import ConnectionHandler, db_session_scope