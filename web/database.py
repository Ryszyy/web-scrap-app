from pymongo import MongoClient
from web.extentions import DB_WRITE_SUCCESSFUL, INPUT_ERROR

client = MongoClient('mongodb://db:27017/sem')
db = client.WebScrap5
resources = db["resources"]



def get_status():
    return "Pending"

def get_resource_by_url(url):
    resource = resources.find_one({"url": url})
    return resource

def get_resource(id):
    resource = resources.find_one({"id": id})
    return resource

def get_resources():
    return resources.find()

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
    resource = get_resource_by_url(url)
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