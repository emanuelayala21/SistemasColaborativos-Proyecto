def setup_periodic_tasks(sender, **kwargs):
    from .tasks import create_periodic_task
    create_periodic_task()
