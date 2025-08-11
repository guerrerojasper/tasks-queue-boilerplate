from .celery import initialize_celery
from .logger import Logger

from config import *

app = initialize_celery()
logger = Logger(
    debug=LOGGER_DEBUG,
    identifier=LOGGER_IDENTIFIER,
    max_bytes=LOGGER_MAX_BYTE,
    backup_count=LOGGER_DEBUG
)

logger.info(f"Celery app started.")

from .dbsession import ConnectionHandler, db_session_scope