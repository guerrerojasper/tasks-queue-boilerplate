import os

class Config(object):
    """Base configuration class."""
    # Celery settings
    CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Default broker (e.g., Redis)
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Default backend
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'
    CELERY_ENABLE_UTC = True

    # Load allowed queues from environment variable CELERY_QUEUES (comma-separated) 
    # E.g., timekeeping,py,report
    # Fallback to default queue if unset
    ALLOWED_QUEUES = os.environ.get('CELERY_QUEUES', '').split(',')
    ALLOWED_QUEUES = [q.strip() for q in ALLOWED_QUEUES if q.strip()] or ['timekeeping']

    # Other settings (e.g., database or logging)

    # Database settings
    DB_USERNAME = os.environ.get('DB_USERNAME', 'user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'pass')
    DB_SERVER = os.environ.get('DB_SERVER', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 5432))
    DB_LIST = os.environ.get('DB_LIST', '').split(',')

    # Logging settings
    LOGGER_DEBUG = False
    LOGGER_IDENTIFIER = "my_celery_app"
    LOGGER_MAX_BYTE = 10485760
    LOGGER_BACKUP_COUNT = 10

class DevelopmentConfig(Config):
    """Development environment configuration."""
    # Celery settings
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1' 

    # Logging settings
    LOGGER_DEBUG = True
    LOGGER_IDENTIFIER = "dev_log"
    LOGGER_MAX_BYTE = 10485760
    LOGGER_BACKUP_COUNT = 5

class ProductionConfig(Config):
    """Production environment configuration."""
    # Celery settings
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

    # Logging settings
    LOGGER_DEBUG = False
    LOGGER_IDENTIFIER = "production_log"
    LOGGER_MAX_BYTE = 10485760
    LOGGER_BACKUP_COUNT = 10


# Load config based on environment (e.g., APP_ENV=development)
env = os.environ.get('APP_ENV', 'development').lower()
config_dict = {
    'development': DevelopmentConfig
}

config = config_dict.get(env, DevelopmentConfig)()