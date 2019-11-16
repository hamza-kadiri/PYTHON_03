import requests
import urllib.parse
from requests import RequestException


# Documentation for the API available at : https://developers.themoviedb.org/3/getting-started/introduction

def init_tmdb_context(app):
    RequestContext.init_request_context(app)


class RequestContext:
    _has_been_initialized = False
    _api_url = None
    _api_key = None
    _thumbnail_base_url = None
    _backdrop_base_url = None
    _poster_base_url = None

    @classmethod
    def init_request_context(cls, app):
        try:
            cls._has_been_initialized = True
            cls._api_url = app.config['API_URL']
            cls._api_key = app.config['API_KEY']
            cls._thumbnail_base_url = app.config['THUMBNAIL_BASE_URL']
            cls._backdrop_base_url = app.config['BACKDROP_BASE_URL']
            cls._poster_base_url = app.config['POSTER_BASE_URL']
        except RuntimeError:
            raise AttributeError(
                "Cannot initialize RequestContext without a proper app configuration")

    @classmethod
    def get_api_url(cls):
        if not cls._has_been_initialized:
            raise AttributeError("Request Context not initialized")
        return cls._api_url

    @classmethod
    def get_api_key(cls):
        if not cls._has_been_initialized:
            raise AttributeError("Request Context not initialized")
        return cls._api_key

    @classmethod
    def get_thumbnail_base_url(cls):
        if not cls._has_been_initialized:
            raise AttributeError("Request Context not initialized")
        return cls._thumbnail_base_url

    @classmethod
    def get_backdrop_base_url(cls):
        if not cls._has_been_initialized:
            raise AttributeError("Request Context not initialized")
        return cls._backdrop_base_url

    @classmethod
    def get_poster_base_url(cls):
        if not cls._has_been_initialized:
            raise AttributeError("Request Context not initialized")
        return cls._poster_base_url


class RequestExceptionOMDB(RequestException):
    def __init__(self, method: str, url: str, http_status_code: int, api_status_message: str, api_status_code: int):
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
    def perform_request(self, endpoint: str, method: str = 'GET', query: str = None):
        if query is not None:
            query_string = f'&query={urllib.parse.quote(query)}'
        else:
            query_string = False
        url = f'{RequestContext.get_api_url()}{endpoint}?api_key={RequestContext.get_api_key()}{query_string or ""}'
        if (method == 'GET'):
            response = requests.get(url)
            if response.status_code != 200:
                raise create_request_exception(method, url, response)
            return response


def create_request_exception(method: str, url: str, resp: any):
    resp2 = resp.json()
    return RequestExceptionOMDB(method, url, resp.status_code, resp2['status_message'], resp2['status_code'])


def search_tv_serie_by_title(query: str):
    endpoint = "/search/tv"
    request = RequestOMDB()
    resp = request.perform_request(endpoint, query=query)
    json = resp.json()
    filteredResults = []
    results = json['results']
    for result in results:
        if result['backdrop_path'] is not None:
            result['thumbnail_url'] = f"{RequestContext.get_backdrop_base_url()}{result['backdrop_path']}"
        if result['poster_path'] is not None:
            result['poster_url'] = f"{RequestContext.get_poster_base_url()}{result['poster_path']}"
            filteredResults.append(result)
    json['results'] = filteredResults
    return json


def get_tv_serie(tv_id: int):
    endpoint = f'/tv/{tv_id}'
    request = RequestOMDB()
    resp = request.perform_request(endpoint)
    json = resp.json()
    if json['backdrop_path'] is not None:
        json['backdrop_url'] = f"{RequestContext.get_backdrop_base_url()}{json['backdrop_path']}"
    return json


def get_tv_serie_season(tv_id: int, season_number: int):
    endpoint = f'/tv/{tv_id}/season/{season_number}'
    request = RequestOMDB()
    resp = request.perform_request(endpoint)
    return resp.json()


def get_tv_serie_episode(tv_id: int, season_number: int, episode_number: int):
    endpoint = f'/tv/{tv_id}/season/{season_number}/episode/{episode_number}'
    request = RequestOMDB()
    resp = request.perform_request(endpoint)
    return resp.json()

def get_tv_genres():
    endpoint = f'/genre/tv/list'
    request = RequestOMDB()
    resp = request.perform_request(endpoint)
    return resp.json()

def get_tv_series_discover():
    endpoint = f'/discover/tv'
    request = RequestOMDB()
    resp = request.perform_request(endpoint)
    return resp.json()

def get_tv_series_discover_by_genre():
    series = get_tv_series_discover()['results']
    genres = get_tv_genres()['genres']
    result = []
    for genre in genres:
        series_concerned = []
        for serie in series:
            try:
                serie['genre_ids'].index(genre['id']) # Raise value error if element not in list
                series_concerned.append({"id":serie['id'],"name":serie['name'],"poster_path":serie['poster_path']})
            except ValueError:
                pass
        if len(series_concerned) > 0:
            result.append({"id":genre['id'],"name":genre['name'],"series":series_concerned})
    return result