from celery import shared_task

@shared_task(queue='queue2', name='runModule02', bind=True)
def task_2(x, y):
    print('Task 2')
    return x * y