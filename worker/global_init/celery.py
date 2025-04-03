from celery import Celery
from kombu import Queue

def initialize_celery():
    app = Celery('celery_app')
    app.config_from_object('config.CeleryConfig')
    app.conf.task_queues = (
        Queue('queue1', routing_key='worker.tasks.module1.tasks.#'),
        Queue('queue2', routing_key='worker.tasks.module2.tasks.#')
    )

    # Discover tasks in the `tasks` module
    app.autodiscover_tasks(['worker.tasks'])

    return app

