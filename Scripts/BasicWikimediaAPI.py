# starting from:
## https://api.wikimedia.org/wiki/Core_REST_API/Reference/Search/Search_titles
## https://api.wikimedia.org/wiki/Core_REST_API/Reference/Pages/Get_page_source
# Author: Phouter0499
# Python 3
# Search English Wikipedia for 5 pages with titles that start with "earth"

import requests

def make_wiki_api_request(url, parameters=None):
    """
    Make an API request to the given URL with the specified parameters.
    Handles exceptions and sets a timeout for the request.

    :param url: The API endpoint URL
    :param parameters: The parameters to be sent with the request
    :return: A JSON response if the request is successful, None otherwise
    """
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
  """
  Searches for titles on Wikipedia based on a search query and returns a list of search results.

  Parameters:
  - search_query (str): The search query to be used for searching titles on Wikipedia.
  - number_of_results (int): The maximum number of search results to be returned.

  Returns:
  - search_results (list): A list of search results. Each search result is a dictionary containing information about a title.

  """
  url = 'https://api.wikimedia.org/core/v1/wikipedia/en/search/title'
  parameters = {'q': search_query, 'limit': number_of_results}

  response = make_wiki_api_request(url, parameters)
  if response is None:
    return []
  search_results = response['pages']

  return search_results

def get_page_source(page_name):
  """
  Get the source code of a Wikipedia page.

  Args:
      page_name (str): The name of the Wikipedia page.

  Returns:
      str: The source code of the Wikipedia page, or None if the page does not exist.
  """
  url = 'https://api.wikimedia.org/core/v1/wikipedia/en/page/' + page_name

  Page_object = make_wiki_api_request(url)
  if Page_object is None:
    return None
  return Page_object

if __name__ == '__main__':
  search_results = search_title('earth', 5)
