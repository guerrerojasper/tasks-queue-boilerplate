from celery import shared_task

@shared_task
def task_2(x, y):
    print('Task 2')
    return x * y