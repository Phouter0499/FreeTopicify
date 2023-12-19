# test_BasicWikimediaAPI.py
import unittest
from BasicWikimediaAPI import make_wiki_api_request, search_title, get_page_source, get_link_texts
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

    def test_get_page_source(self):
        search_results = search_title('earth', 1)
        page_source = get_page_source(search_results[0]['key'])
        self.assertIsNotNone(page_source)
        # write page_source to file
        with open('page_source.html', 'w', encoding="utf-8") as f:
            f.write(page_source)

    def test_mwparserfromhell(self):
        search_results = search_title('earth', 1)
        page_source = get_page_source(search_results[0]['key'])
        parsed_wikitext = mwparserfromhell.parse(page_source)
        sections = parsed_wikitext.get_sections()
        #breakpoint()
    
    def test_get_link_texts(self):
        search_results = search_title('earth', 1)
        page_source = get_page_source(search_results[0]['key'])
        link_texts = get_link_texts(page_source)
        print(link_texts)

if __name__ == '__main__':
    unittest.main()
