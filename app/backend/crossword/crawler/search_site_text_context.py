from bs4 import BeautifulSoup
from bs4.element import Comment
import requests

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

class Page_Text:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0'
        }

    def text_from_html(self, body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)  
        return u" ".join(t.strip() for t in visible_texts)

    def get_content(self, url: str) -> str:
        html = requests.get(url, headers=self.headers)
        return self.text_from_html(html.content)
