# starting from:
## https://api.wikimedia.org/wiki/Core_REST_API/Reference/Search/Search_titles
## https://api.wikimedia.org/wiki/Core_REST_API/Reference/Pages/Get_page_source
# Author: Phouter0499
# Python 3
# Search English Wikipedia for 5 pages with titles that start with "earth"

import requests
import mwparserfromhell
import re

def make_wiki_api_request(url, parameters=None):
    try:
        response = requests.get(url, params=parameters, timeout=60)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(response)
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(response)
        print(f"Error connecting to the server: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(response)
        print(f"Timeout error: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(response)
        print(f"Unexpected error occurred: {req_err}")
    return None

def search_title(search_query, number_of_results):
  url = 'https://api.wikimedia.org/core/v1/wikipedia/en/search/title'
  parameters = {'q': search_query, 'limit': number_of_results}

  response = make_wiki_api_request(url, parameters)
  if response is None:
    return []
  search_results = response['pages']

  return search_results

def get_page_source(page_name):
  url = 'https://api.wikimedia.org/core/v1/wikipedia/en/page/' + page_name

  Page_object = make_wiki_api_request(url)
  if Page_object is None:
    return None
  return Page_object['source']

def get_link_texts(page_source):
  parsed_wikitext = mwparserfromhell.parse(page_source)
  for template in parsed_wikitext.filter_templates():
    try:
      parsed_wikitext.remove(template)
    except ValueError:
      pass
  sections = parsed_wikitext.get_sections()
  wikilinks = []
  for section in sections:
    wikilinks += section.filter_wikilinks()
  wikilink_texts = [link.title for link in wikilinks]
  # convert into str
  wikilink_texts = [str(l) for l in wikilink_texts if len(l) > 0]
  # deal with 'globus cruciger (fixed width).svg'
  # deal with 'Category:Astronomical objects known since antiquity'
  wikilink_texts = [l for l in wikilink_texts if not re.match(r':[a-zA-Z]+:|[a-zA-Z]+:', l)]
  # deal with inner links '#Axial tilt and seasons'
  wikilink_texts = [l[1:] if l[0] == '#' else l for l in wikilink_texts]
  # deal with 'Water vapor#In Earth's atmosphere' or 'Cloud#Formation' or 'Capitalization in English#History of English capitalization'
  wikilink_texts = [re.split(r'#', l, 1)[0] if re.search(r'#', l) else l for l in wikilink_texts]
  return list(set(wikilink_texts))

if __name__ == '__main__':
  search_results = search_title('earth', 5)
