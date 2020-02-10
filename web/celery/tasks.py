from web.app import make_celery, app

celery = make_celery(app)

