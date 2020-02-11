from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from web.celery_instance import celery
from web.database import add_text_to_resource, add_images_to_resource


def url_parse(url):
    if "http://" in url:
        http_url = url
        url = url[7:]
    else:
        http_url = "http://" + url
    return http_url, url


@celery.task()
def get_website_text(url):
    http_url, url = url_parse(url)
    html = urlopen(http_url).read()
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text(separator=' ')

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return add_text_to_resource(url, text)


@celery.task()
def get_website_images(url):
    images = []
    http_url, url = url_parse(url)
    html = requests.get(http_url)

    soup = BeautifulSoup(html.text, 'html.parser')
    img_tags = soup.find_all('img')

    img_urls = [img['src'] for img in img_tags]

    for i, img_url in enumerate(img_urls):
        with open(str(i), 'wb+') as f:
            if 'http' not in img_url:
                img_url = f'{http_url}{img_url}'

            response = requests.get(img_url)
            images.append(response.content)

    return add_images_to_resource(url, images)

