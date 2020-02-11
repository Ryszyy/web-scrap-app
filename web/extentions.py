def template(code, data):
    return {'status_code': code, 'message': data}


DB_WRITE_SUCCESSFUL = template(200, "Write to db successful")
DB_WRITE_FAILED = template(300, "Write to db was not successful")

INPUT_ERROR = template(400, "Data input error")
ITEM_NOT_FOUND = template(404, "Item not found")