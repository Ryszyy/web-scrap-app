from bson import ObjectId
from pymongo import MongoClient
from gridfs import GridFS
from web.extentions import DB_WRITE_SUCCESSFUL, ITEM_EXIST_IN_DB


client = MongoClient('mongodb://db:27017/sem')
db = client.WebScrap7
resources = db["resources"]
fs = GridFS(db)


def get_status():
    return "Pending"


def get_resource_by_url(url: str):
    resource = resources.find_one({"url": url})
    return resource


def get_resource(id: str):
    resource = resources.find_one({"id": int(id)})
    return resource


def get_all_resources():
    return resources.find()


def url_resource_exist(url: str):
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


def update_images(url: str, links: list):
    resources.update_one(
        {
            "url": url,
        }, {
            "$set": {
                "images": links
            }
        })


def add_text_to_resource(url: str, text: str):
    resource = get_resource_by_url(url)
    if resource:
        if resource["text"]:
            return "text exists"
        update_resource(url, "text", text)
    else:
        create_resource(url, text=text)
    return None


def add_images_to_resource(url: str, images: list):
    """
    adding images to the existing resource or
    creating resource with provided images
    :param url: string
    :param images: list of binaries
    :return: None
    """
    resource = get_resource_by_url(url)
    if resource:
        if resource["images"]:
            return ITEM_EXIST_IN_DB
        links = save_images(images)
        update_images(url, links)
    else:
        links = save_images(images)
        create_resource(url, images=links)
    return None


def create_resource(url, text=None, images=None):
    resources.insert_one(
        {
            "id": resources.count_documents({}) + 1,
            "url": url,
            "text": text,
            "images": images
        })
    return None


def save_images(images: list):
    """
    :param images: list of binaries
    :return: list of strings oid's
    """
    return [str(fs.put(x)) for x in images]


def get_image(oid: str):

    return fs.get(ObjectId(oid)).read()
    # return resources.find_one({"_id": oid})