from flask import jsonify, request
from marshmallow import Schema, fields
from flask_restful import Resource
from urllib.error import URLError
from web.extentions import DB_WRITE_SUCCESSFUL, INPUT_ERROR, ITEM_NOT_FOUND, DB_WRITE_FAILED
from web.database import get_resource, get_resources, add_resource
from web.tasks import get_website_text


class ResourcesSchema(Schema):
    id = fields.Integer()
    url = fields.String()
    text = fields.String()
    images = fields.List(fields.String())

    class Meta:
        fields = ("id", "url", "text", "images")
        ordered = True


schema = ResourcesSchema()

# @api.route('/resources/<ids>')
class WebScrap(Resource):
    def get(self, ids):
        # res = resources.find_one({"id": int(ids)})
        res = get_resource(ids)

        if res is None:
            return ITEM_NOT_FOUND
        ret = schema.dump(res)
        return ret

    def put(self, ids=None):
        requested_data = request.get_json()
        try:
            # res = resources.find_one({"id": int(ids)})
            res = get_resource(ids)
            if res is None:
                return ITEM_NOT_FOUND

            # res.update(**requested_data)
            return DB_WRITE_SUCCESSFUL
        except TypeError:
            return DB_WRITE_FAILED


# @api.route('/resources')
class WebScrapText(Resource):
    def get(self):
        all_res = get_resources()
        x = [{"id": x["id"], "url":x["url"]} for x in all_res]
        return x

    def post(self):
        request_data = request.get_json()
        try:
            url = request_data["url"]
            text = get_website_text.delay(url)
            # resources.save_file()
        except (TypeError, ValueError, URLError):
            """
            no url keyword
            wrong url format
            url does not exist
            """
            return INPUT_ERROR

        return add_resource(url, text=text)


# @api.route('/pending')
# class WebScrapStatus(Resource):
#     def get(self):
#         all_res = resources.find({"status": "Pending"})
#         x = [{"id": x["id"], "url":x["url"], "status": x["status"]} for x in all_res]
#         return x