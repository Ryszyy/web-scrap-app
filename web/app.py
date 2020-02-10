from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from marshmallow import Schema, fields
from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
from celery import Celery

import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

CELERY_TASK_LIST = [
    "celery.tasks"
]


def make_celery(flask_app):
    celery_app = Celery(
        flask_app.import_name,
        backend=flask_app.config['CELERY_RESULT_BACKEND'],
        broker=flask_app.config['CELERY_BROKER_URL'],
        include=CELERY_TASK_LIST
    )
    celery_app.conf.update(flask_app.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


app = Flask(__name__)
app.config.update(
    TESTING=True,
    CELERY_BROKER_URL='redis://redis:6379/0',
    CELERY_RESULT_BACKEND='redis://redis:6379/0'
)

celery = make_celery(app)


api = Api(app)

client = MongoClient('mongodb://db:27017/sem')
db = client.WebScrap5
resources = db["resources"]
# cache = redis.Redis(host='redis', port=6379)


class ResourcesSchema(Schema):
    id = fields.Integer()
    url = fields.String()
    text = fields.String()
    images = fields.List(fields.String())

    class Meta:
        fields = ("id", "url", "text", "images")
        ordered = True


schema = ResourcesSchema()

@celery.task()
def get_website_text(url):
    http_url = "http://" + url
    html = urlopen(http_url).read()
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text(separator=' ')

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def template(code, data):
    return {'status_code': code, 'message': data}


DB_WRITE_SUCCESSFUL = template(200, "Write to db successful")
DB_WRITE_FAILED = template(300, "Write to db was not successful")

INPUT_ERROR = template(400, "Data input error")
ITEM_NOT_FOUND = template(404, "Item not found")


def get_status():
    return "Pending"


def get_resource(url):
    resource = resources.find_one({"url": url})
    return resource


def resource_exist(url):
    resource = resources.find_one({"url": url})
    return True if resource else False


def update_resource(url: str, res_type: str, data):
    update_dict = {res_type: data}
    resources.update_one(
        {
            "url": url,
        }, {
            "$set": update_dict
        })


def add_resource(url, text=None, images=None):
    resource = get_resource(url)
    if not resource:
        resources.insert_one(
            {
                "id": resources.count_documents({}) + 1,
                "url": url,
                "text": text,
                "images": images,
                "status": get_status()
            })
        return DB_WRITE_SUCCESSFUL
    else:
        return INPUT_ERROR



# @api.route('/resources/<ids>')
class WebScrap(Resource):
    def get(self, ids):
        res = resources.find_one({"id": int(ids)})
        if res is None:
            return ITEM_NOT_FOUND
        ret = schema.dump(res)
        return ret

    def put(self, ids=None):
        requested_data = request.get_json()
        try:
            res = resources.find_one({"id": int(ids)})
            if res is None:
                return ITEM_NOT_FOUND

            # res.update(**requested_data)
            return DB_WRITE_SUCCESSFUL
        except TypeError:
            return DB_WRITE_FAILED


# @api.route('/resources')
class WebScrapText(Resource):
    def get(self):
        all_res = resources.find()
        x = [{"id": x["id"], "url":x["url"]} for x in all_res]
        return x

    def post(self):
        request_data = request.get_json()
        try:
            url = request_data["url"]
            text = get_website_text.delay(url)
            resources.save_file()
        except (TypeError, ValueError, URLError):
            """
            no url keyword
            wrong url format
            url does not exist
            """
            return INPUT_ERROR

        return add_resource(url, text=text)


# @api.route('/pending')
class WebScrapStatus(Resource):
    def get(self):
        all_res = resources.find({"status": "Pending"})
        x = [{"id": x["id"], "url":x["url"], "status": x["status"]} for x in all_res]
        return x


api.add_resource(WebScrap, '/resources/<ids>')
api.add_resource(WebScrapText, '/resources')
api.add_resource(WebScrapStatus, '/pending')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
