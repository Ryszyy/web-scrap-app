from web import views


def initialize_routes(api):
    api.add_resource(views.WebScrap, '/api/resources', '/api/resources/<ids>')
    # api.add_resource(views.WebScrapText, '/api/resources/text')
    api.add_resource(views.WebScrapImages, '/api/resources/<id>/<oid>')
