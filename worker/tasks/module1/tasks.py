from celery import shared_task

@shared_task(queue='queue1', name='runModule01', bind=True)
def task_1(x, y):
    print('task_1')
    return x + y