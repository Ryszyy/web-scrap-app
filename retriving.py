from urllib import request
from bs4 import BeautifulSoup

url = "http://www.saf.com"
html = request.urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

for script in soup(["script", "style"]):
    script.extract()

text = soup.get_text(separator=' ')

lines = (line.strip() for line in text.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
text = '\n'.join(chunk for chunk in chunks if chunk)

print(text)