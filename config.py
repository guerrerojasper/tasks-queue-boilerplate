LOGGER_DEBUG = False
LOGGER_IDENTIFIER = "my_celery_app"
LOGGER_MAX_BYTE = 10485760
LOGGER_BACKUP_COUNT = 5

class CeleryConfig(object):
    broker_url = 'redis://localhost:6379/1'
    result_backend = 'redis://localhost:6379/0'