# from web.app import make_celery
from run import celery
from urllib.request import urlopen
from bs4 import BeautifulSoup

# celery = make_celery()

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