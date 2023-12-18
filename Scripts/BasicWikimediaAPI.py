# starting from
# https://api.wikimedia.org/wiki/Core_REST_API/Reference/Search/Search_titles
# Author: Phouter0499
# Python 3
# Search English Wikipedia for 5 pages with titles that start with "earth"

import requests

def make_wiki_api_request(url, parameters):
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
  Retrieves a specified number of search results from the Wikipedia API based on a given search query.

  Parameters:
    - search_query (str): The search query to be used for retrieving the search results.
    - number_of_results (int): The number of search results to be retrieved.

  Returns:
    - pages: A list of dictionaries representing the search result pages from the Wikipedia API.
    to understand output better: https://api.wikimedia.org/wiki/Core_REST_API/Reference/Search/Search_result_object
  """
  url = 'https://api.wikimedia.org/core/v1/wikipedia/en/search/title'
  parameters = {'q': search_query, 'limit': number_of_results}

  response = make_wiki_api_request(url, parameters)
  if response is None:
    return []
  pages = response['pages']

  return pages

if __name__ == '__main__':
  pages = search_title('earth', 5)
  for page in pages:
    print(page['title'])
    print(page['description'])
    print()