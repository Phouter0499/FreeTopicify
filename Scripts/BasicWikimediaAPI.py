# starting from:
## https://api.wikimedia.org/wiki/Core_REST_API/Reference/Search/Search_titles
## https://api.wikimedia.org/wiki/Core_REST_API/Reference/Pages/Get_page_source
## https://en.wikipedia.org/wiki/Help:Link
# Author: Phouter0499
# Python 3
# Search English Wikipedia for 5 pages with titles that start with "earth"

import requests
import re
from bs4 import BeautifulSoup

def make_wiki_api_request(url, parameters=None):
    try:
        response = requests.get(url, params=parameters, timeout=60)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response
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
  if not response:
    return []
  search_results = response.json()['pages']

  return search_results

def search_content(search_query, number_of_results):
  url = 'https://api.wikimedia.org/core/v1/wikipedia/en/search/page'
  parameters = {'q': search_query, 'limit': number_of_results}

  response = make_wiki_api_request(url, parameters)
  if not response:
    return []
  search_results = response.json()['pages']

  return search_results

def get_html(title, project='wikipedia', language='en'):
  url = f'https://api.wikimedia.org/core/v1/{project}/{language}/page/{title}/html'

  response = make_wiki_api_request(url)
  if not response:
    print(response)
    return None
  HTML = response.text
  return HTML

def get_link_texts(html):
  soup = BeautifulSoup(html, 'lxml')
  # get the section with references from the wikipage and delete its parents recursively
  heading = soup.find(id='References')
  heading.parent.decompose()
  # get the section with notes from the wikipage and delete its parents recursively
  heading = soup.find(id='Notes')
  heading.parent.decompose()
  # get all wikilinks from a wikipage
  wikilinks = soup.find_all('a', rel=re.compile('mw:WikiLink'), href=re.compile(r'\.\/.+?'), title=True)
  # get text from the wikilink while filtering for 
  wikilink_titles = []
  for link in wikilinks:
    title = link['title']
    if re.match(r"Portal:", title):
      title = title[7:]
    elif ":" in title:
      continue
    wikilink_titles.append(title)
  return wikilink_titles

if __name__ == '__main__':
  search_results = search_title('earth', 5)
