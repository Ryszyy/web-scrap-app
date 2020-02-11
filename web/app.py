from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from celery import Celery
from web.


def make_celery(flask_app=None):
    app = flask_app or create_app()
    celery_app = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include="web.tasks"
    )
    celery_app.conf.update(app.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app

def create_app():
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        CELERY_BROKER_URL='redis://redis:6379/0',
        CELERY_RESULT_BACKEND='redis://redis:6379/0'
    )
    return app

def extentions(app):
    api = Api(app)

    api.add_resource(WebScrap, '/resources/<ids>')
    api.add_resource(WebScrapText, '/resources')
    api.add_resource(WebScrapStatus, '/pending')
    return None
