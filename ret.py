import re
import requests
from bs4 import BeautifulSoup

url = "http://ocdn.eu/pulscms-transforms/1/qW_ktkpTURBXy83OGJkMDg3MTVjMDVmOTc5NzI0MGZiYmY2OGMyMGVkZS5qcGeTlQMlXs0FkM0DIpMFzQEszKiVB9kyL3B1bHNjbXMvTURBXy83MWUxOGYwMDNhYWE1ODk3NTIwMmFmNTk0OGZmNmZjMS5wbmcAwgA"

with open("test", 'wb+') as f:
    response = requests.get(url)
    f.write(response.content)
