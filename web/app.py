from flask import Flask
from web.routes import initialize_routes
from flask_restful import Api
from web.celery_instance import celery, init_celery


def create_app():
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        CELERY_BROKER_URL='redis://redis:6379/0',
        CELERY_RESULT_BACKEND='redis://redis:6379/0',
        CELERY_TASKS="web.tasks"
    )
    init_celery(celery, app)
    api = Api()
    initialize_routes(api)
    api.init_app(app)
    return app


