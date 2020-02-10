import re
import requests
from bs4 import BeautifulSoup
from requests.exceptions import MissingSchema, InvalidURL

site = 'http://www.facebook.com'

response = requests.get(site)

soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')

urls = [img['src'] for img in img_tags]

for i, url in enumerate(urls):
    with open(str(i), 'wb+') as f:
        if 'http' not in url:
            url = f'{site}{url}'

        response = requests.get(url)
        f.write(response.content)

