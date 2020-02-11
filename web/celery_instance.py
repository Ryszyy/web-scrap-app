from celery import Celery


def make_celery(app_name=__name__):
    return Celery(app_name,
                  backend="redis://redis:6379/0",
                  broker="redis://redis:6379/0")


celery = make_celery()


def init_celery(celery, app):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
