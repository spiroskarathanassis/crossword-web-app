import re

from bs4 import BeautifulSoup
import requests

from ..helpers.regex import choose_part_of_definition

class GoogleSpider(object):
    def __init__(self):
        """Crawl Google search results

        This class is used to crawl Google's search results using requests and BeautifulSoup.
        """
        super().__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Host': 'www.google.com',
            'Referer': 'https://www.google.com/'
        }

    def __get_source(self, url: str) -> requests.Response:
        """Get the web page's source code

        Args:
            url (str): The URL to crawl

        Returns:
            requests.Response: The response from URL
        """
        return requests.get(url, headers=self.headers)

    def search(self, query: str) -> list:
        """Search Google

        Args:
            query (str): The query to search for

        Returns:
            list: { title, url } -- The search results
        """
        MAX_RESULTS = '20'
        query = query.replace(' ', '+')

        response = self.__get_source(f'https://www.google.com/search?hl=en&lr=lang_en&q={query}&num={MAX_RESULTS}')
        soup = BeautifulSoup(response.text, 'html.parser')
        result_containers = soup.find(id="rso") # id='search' -> id='rso'
        result_containers = result_containers.findAll('div', class_='g')
        
        results = []
        for container in result_containers:
            # Result title
            title = container.find('h3')
            # Result URL
            url = container.find('a')['href']
            if not(url and title): continue

            results.append({
                'title': title.text,
                'url': url,
            })

        return results

    def search_doc_definition(self, query: str) -> str:
        """Search Google

        Args:
            query (str): The query to search for

        Returns:
            list: The search result text of wiki definition
        """
        result = ''
        MAX_RESULTS = '20'

        try:
            response = self.__get_source(f'https://www.google.com/search?hl=en&lr=lang_en&q={query}&num={MAX_RESULTS}')
            soup = BeautifulSoup(response.text, 'html.parser')
            result_containers = soup.find(id="kp-wp-tab-overview")
            
            # search for right definition of google
            if result_containers:
                descr_element = result_containers.find("h3")
                result = descr_element.find_next("span")
                
                if result:
                    return choose_part_of_definition(result.text)
            
            result_containers = soup.find(id="rso")
            result_containers = result_containers.findAll('div', class_='g')
            
            for container in result_containers:
                container = container.find('div', class_='IsZvec')
                
                # Result description
                des = container.find('span')
                des_texts = des.findAll(text=True)
                
                # join text of elements
                res = ''.join(des_texts)
                res = re.split('. ', res)

                if res[0]:
                    return res[0]
            
            return ""
        except:
            return ""
