from config import config
from .logger import logger
from .celery import initialize_celery
from .dbsession import ConnectionHandler, db_session_scope

app = initialize_celery()
logger.info(f"Celery app started.")
