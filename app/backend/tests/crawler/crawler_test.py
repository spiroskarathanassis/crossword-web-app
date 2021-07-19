import unittest

import sys
sys.path.append('./app/backend/')

from crossword.crawler.search_site_text_context import Page_Text
from crossword.crawler.search_google import GoogleSpider

class TestNeighorhood(unittest.TestCase):
  def test_crawled_theme_word_collection(self):
    theme = 'animals'
    crawled_theme_words = Crawler().collect_all_crawled_theme_words(theme)
    
    self.assertIsNotNone(crawled_theme_words)

  def test_google_crawl_urls(self):
    theme = 'developer'
    result_list = GoogleSpider().search(theme)

    self.assertNotEqual(len(result_list), 0)

  def test_utl_page_text(self):
    url = 'https://laraveldaily.com/test-junior-laravel-developer-sample-project/'
    content = Page_Text().get_content(url)
    
    self.assertIsNotNone(content)

if __name__ == '__main__':
  unittest.main()