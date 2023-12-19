# test_BasicWikimediaAPI.py
import unittest
from BasicWikimediaAPI import make_wiki_api_request, search_title, get_html, get_link_texts
import mwparserfromhell

class TestBasicWikimediaAPI(unittest.TestCase):

    def test_make_wiki_api_request(self):
        url = 'https://api.wikimedia.org/core/v1/wikipedia/en/search/title'
        parameters = {'q': 'earth', 'limit': 5}
        response = make_wiki_api_request(url, parameters)
        self.assertIsNotNone(response)

    def test_search_title(self):
        search_results = search_title('earth', 5)
        for search_result in search_results:
            print(search_result['title'])
            print(search_result['description'])
            print()

    def test_get_html(self):
        search_results = search_title('earth', 1)
        html_page = get_html(search_results[0]['key'])
        self.assertIsNotNone(html_page)
        # write page_source to file
        with open('html_page.html', 'w', encoding="utf-8") as f:
            f.write(html_page)
    
    def test_get_link_texts(self):
        search_results = search_title('earth', 1)
        html = get_html(search_results[0]['key'])
        link_texts = get_link_texts(html)
        print(set(link_texts))

if __name__ == '__main__':
    unittest.main()
