from celery import shared_task

@shared_task
def task_1(x, y):
    print('task_1')
    return x + y