# test_BasicWikimediaAPI.py
import unittest
from BasicWikimediaAPI import *
import re
import spacy
from wordfreq import zipf_frequency

class TestBasicWikimediaAPI(unittest.TestCase):

    def test_make_wiki_api_request(self):
        url = 'https://api.wikimedia.org/core/v1/wikipedia/en/search/title'
        parameters = {'q': 'earth', 'limit': 5}
        response = make_wiki_api_request(url, parameters)
        self.assertIsNotNone(response)

    def test_search_title(self):
        search_results = search_title('earth', 5)
        pairs = []
        for search_result in search_results:
            pairs.append((search_result['title'], search_result['description']))
        print(pairs)

    def test_search_content(self):
        with open("The Prospect of AI in the Workforce; A 50-Year Outlook.txt", "r", encoding="utf-8") as f:
            essay = f.read()
        # get list of nouns using spacy
        nlp = spacy.load("en_core_web_lg")
        doc = nlp(essay)
        nouns = list({token.lemma_ for token in doc if token.pos_ == "NOUN" and re.search(r"\w", token.lemma_)})
        sorted_N = sorted(nouns, key=lambda x: zipf_frequency(x, 'en'), reverse=False)
        query = ""
        for noun in sorted_N:
            temp_query = f"{query} OR {noun}" if query else noun
            if len(temp_query) <= 300:
                query = temp_query
            else:
                break
        print(query)
        search_results = search_content(query, 15)
        pairs = []
        for search_result in search_results:
            pairs.append((search_result['title'], search_result['description']))
        print(pairs)

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
