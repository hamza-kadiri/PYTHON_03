import requests
import urllib.parse
from requests import RequestException
from flask import current_app as app


# Documentation for the API available at : https://developers.themoviedb.org/3/getting-started/introduction

# TODO : Delete single pattern ?
class RequestExceptionOMDB(RequestException):
    def __init__(self, method, url, http_status_code, api_status_message, api_status_code):
        RequestException.__init__(
            self, '{} {} {}'.format(method, url, http_status_code))
        self.__method = method
        self.__url = url
        self.__http_status_code = http_status_code
        self.__api_status_message = api_status_message
        self.__api_status_code = api_status_code

    @property
    def method(self):
        return self.__method

    @property
    def url(self):
        return self.__url

    @property
    def http_status_code(self):
        return self.__http_status_code

    @property
    def api_status_message(self):
        return self.__api_status_message

    @property
    def api_status_code(self):
        return self.__api_status_code


class RequestOMDB:
    class __RequestOMDB:
        def __init__(self):
            try:
                self._base_url = app.config['API_URL']
                self._api_key = app.config['API_KEY']
            except RuntimeError:
                raise AttributeError(
                    "Cannot instantiate RequestOMDB without the app context")

        @property
        def base_url(self):
            return self._base_url

        @property
        def api_key(self):
            return self._api_key

        def perform_request(self, endpoint: str, method='GET', query=None):
            queryString=""
            if query is not None:
                queryString = f'&query={urllib.parse.quote(query)}'
            url = f'{self.base_url}{endpoint}?api_key={self.api_key}{queryString}'
            if (method == 'GET'):
                print(url)
                response = requests.get(url)
                print(response)
                if response.status_code != 200:
                    raise create_request_exception(method, url, response)
                return response

    instance = None

    def __init__(self):
        try:
            self._base_url = app.config['API_URL']
            self._api_key = app.config['API_KEY']
        except RuntimeError:
            raise AttributeError(
                "Cannot instantiate RequestOMDB without the app context")

    @property
    def base_url(self):
        return self._base_url

    @property
    def api_key(self):
        return self._api_key

    def perform_request(self, endpoint: str, method='GET', query=None):
        if query is not None:
            query_string = f'&query={urllib.parse.quote(query)}'
            print(query_string)
        else:
            query_string = False
        url = f'{self.base_url}{endpoint}?api_key={self.api_key}{query_string  or ""}'
        print(url)
        if (method == 'GET'):
            response = requests.get(url)
            if response.status_code != 200:
                raise create_request_exception(method, url, response)
            return response


def create_request_exception(method, url, resp):
    resp2 = resp.json()
    return RequestExceptionOMDB(method, url, resp.status_code, resp2['status_message'], resp2['status_code'])


def search_tv_serie_by_title(query: str):
    endpoint = "/search/tv"
    request = RequestOMDB()
    resp = request.perform_request(endpoint, query=query)
    json = resp.json()
    results = json['results']
    for result in results:
        result['thumbnail_url'] = f"{app.config['THUMBNAIL_BASE_URL']}{result['backdrop_path']}"
    json['results'] = results
    return json


def get_tv_serie(tv_id: int):
    endpoint = f'/tv/{tv_id}'
    request = RequestOMDB()
    resp = request.perform_request(endpoint)
    json = resp.json()
    json['backdrop_url'] = f"{app.config['BACKDROP_BASE_URL']}{json['backdrop_path']}"
    return json


# noinspection PyInterpreter
def get_tv_serie_episode(tv_id: int, season_number: int, episode_number: int):
    endpoint = f'/tv/{tv_id}/season/{season_number}/episode/{episode_number}'
    request = RequestOMDB()
    resp = request.perform_request(endpoint)
    return resp.json()