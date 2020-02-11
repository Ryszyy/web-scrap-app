from flask import jsonify, request
from marshmallow import Schema, fields
from flask_restful import Resource
from urllib.error import URLError
from web.extentions import DB_WRITE_SUCCESSFUL, INPUT_ERROR, ITEM_NOT_FOUND, DB_WRITE_FAILED, PROCESSING_TASK
from web.database import get_resource, get_all_resources, get_image
from web.tasks import get_website_text, get_website_images


class MinimalResourcesSchema(Schema):
    id = fields.Integer()
    url = fields.String()

    class Meta:
        fields = ("id", "url")
        ordered = True


class ResourcesSchema(MinimalResourcesSchema):
    text = fields.String()
    images = fields.List(fields.String())

    class Meta:
        fields = ("id", "url", "text", "images")
        ordered = True


schema = ResourcesSchema()
minimal_schema = MinimalResourcesSchema()


class WebScrap(Resource):
    def get(self, ids=None):
        """
        :param ids: id of resource
        :return: single resource if ids is provided, else return all resources
        """
        try:
            res = get_resource(ids)
            ret = schema.dump(res)
            if res is None:
                return ITEM_NOT_FOUND
        except TypeError:
            res = get_all_resources()
            ret = [schema.dump(x) for x in res]
        return ret

    def post(self):
        """
        :except url format: "www.google.com" or "http://www.google.com"
                res_type must be:
                - "text"
                - "images"
        :return: status of post method
        """
        request_data = request.get_json()
        try:
            url = request_data["url"]
            res_type = request_data["type"]

            if res_type == "text":
                result = get_website_text.delay(url)
            elif res_type == "images":
                result = get_website_images.delay(url)
            else:
                return INPUT_ERROR

            if result.ready():
                return result.get()
        except (TypeError, ValueError, URLError):
            """
            - no url provided
            - wrong url format
            - url does not exist
            """
            return INPUT_ERROR
        else:
            return PROCESSING_TASK


class WebScrapImages(Resource):
    def get(self, id=None, oid=None):
        print(id, oid, flush=True)
        image = get_image(oid)
        return image

# class WebScrapText(Resource):
#     def post(self):
#         request_data = request.get_json()
#         try:
#             url = request_data["url"]
#             result = get_website_text.delay(url)
#             if result.ready():
#                 return result.get()
#         except (TypeError, ValueError, URLError):
#             """
#             no url keyword
#             wrong url format
#             url does not exist
#             """
#             return INPUT_ERROR
#         else:
#             return PROCESSING_TASK
#
#
# class WebScrapImages(Resource):
#     def post(self):
#         request_data = request.get_json()
#         try:
#             url = request_data["url"]
#             result = get_website_text.delay(url)
#             if result.ready():
#                 return result.get()
#         except (TypeError, ValueError, URLError):
#             """
#             no url keyword
#             wrong url format
#             url does not exist
#             """
#             return INPUT_ERROR
#         else:
#             return PROCESSING_TASK

# @api.route('/pending')
# class WebScrapStatus(Resource):
#     def get(self):
#         all_res = resources.find({"status": "Pending"})
#         x = [{"id": x["id"], "url":x["url"], "status": x["status"]} for x in all_res]
#         return x



    # def put(self, ids=None):
    #     requested_data = request.get_json()
    #     try:
    #         res = get_resource(ids)
    #         if res is None:
    #             return ITEM_NOT_FOUND
    #
    #         # res.update(**requested_data)
    #         return DB_WRITE_SUCCESSFUL
    #     except TypeError:
    #         return DB_WRITE_FAILED