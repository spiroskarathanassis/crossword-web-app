import re

from .search_google import GoogleSpider
from .search_site_text_context import Page_Text
from .keep_theme_crawled import Search_Similarity

class Crawler:
  def __init__(self) -> None:
    self.crawled_words = set()
    self.url_list = []
    self.theme = ''
  
  def collect_all_crawled_theme_words(self, theme: str) -> list:
    self.theme = theme
    self.collect_crawled_urls()
    self.adjust_words_from_url_list_body()
    
    return list(self.crawled_words)

  def collect_crawled_urls(self):
    """Collect urls and save {4} because of big time complexity"""

    url_list = GoogleSpider().search(self.theme)
    
    # TODO: can be random from url_list
    self.url_list = url_list[2:6]

  def adjust_words_from_url_list_body(self):
    for url in self.url_list:
      domain_url = url.get('url')
      print('Collect words from url', domain_url)

      content = Page_Text().get_content(domain_url)
      
      # delete extra spaces
      content = re.sub(' +',' ', content)
      
      # split context into sentences
      sentences = re.split('! |\. |\? |; ', content)

      # search theme similarity and save words
      similarity = Search_Similarity()
      mathced_words_similar = []

      for sentence in sentences:
        mathced_words_similar = similarity.similar_percentage(self.theme, sentence)
        if len(mathced_words_similar) != 0:
          self.crawled_words.update(mathced_words_similar)