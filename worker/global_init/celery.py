from celery import Celery
from kombu import Queue
from config import config
from . import logger

def initialize_celery():
    app = Celery(
        'celery_app',
        broker=config.CELERY_BROKER_URL,
        backend=config.CELERY_RESULT_BACKEND,
        include=['worker.tasks']
    )
    # logger.info("Initializing celery app.")
    # logger.info(f"Broker: {config.CELERY_BROKER_URL}")
    # logger.info(f"Backend: {config.CELERY_RESULT_BACKEND}")

    # Load configuration from config class
    app.conf.update(
        accept_content=config.CELERY_ACCEPT_CONTENT,
        task_serializer=config.CELERY_TASK_SERIALIZER,
        result_serializer=config.CELERY_RESULT_SERIALIZER,
        timezone=config.CELERY_TIMEZONE,
        enable_utc=config.CELERY_ENABLE_UTC,
    )

    # Configure queues from ALLOWED_QUEUES
    app.conf.task_queues = {
        queue: {} for queue in config.ALLOWED_QUEUES
    }
    print(app.conf.task_queues)
    # app_queues = {
    #     ('queue1', 'worker.tasks.module1.tasks.#'),
    #     ('queue2', 'worker.tasks.module2.tasks.#')
    # }
    # app.conf.task_queues = (
    #     Queue('queue1', routing_key='worker.tasks.module1.tasks.#'),
    #     Queue('queue2', routing_key='worker.tasks.module2.tasks.#')
    # )

    return app

