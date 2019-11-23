import requests
import urllib.parse
from requests import RequestException
from helpers import generate_assets_url


# Documentation for the API available at : https://developers.themoviedb.org/3/getting-started/introduction

def init_tmdb_context(app):
    RequestContext.init_request_context(app)


class RequestContext:
    __has_been_initialized = False
    __api_url = None
    __api_key = None

    @classmethod
    def init_request_context(cls, app):
        try:
            cls.__has_been_initialized = True
            cls.__api_url = app.config['API_URL']
            cls.__api_key = app.config['API_KEY']
        except RuntimeError:
            raise AttributeError(
                "Cannot initialize RequestContext without a proper app configuration")

    @classmethod
    def get_api_url(cls):
        if not cls.__has_been_initialized:
            raise AttributeError("Request Context not initialized")
        return cls.__api_url

    @classmethod
    def get_api_key(cls):
        if not cls.__has_been_initialized:
            raise AttributeError("Request Context not initialized")
        return cls.__api_key


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
            query_string = query
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
    query_string = f'&query={urllib.parse.quote(query)}'
    resp = request.perform_request(endpoint, query=query_string)
    json = resp.json()
    for result in json['results']:
        generate_assets_url(result)
    return json


def get_tv_serie(tv_id: int):
    endpoint = f'/tv/{tv_id}'
    request = RequestOMDB()
    resp = request.perform_request(endpoint)
    json = resp.json()
    generate_assets_url(json)
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
    query = "language=en-US&sort_by=popularity.desc&air_date.gte=1573992374&page=1&timezone=America%2FNew_York&include_null_first_air_dates=false"
    request = RequestOMDB()
    resp = request.perform_request(endpoint,query=query)
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
                generate_assets_url(serie)
                series_concerned.append(serie)
            except ValueError:
                pass
        if len(series_concerned) > 0:
            result.append({"id":genre['id'],"name":genre['name'],"series":series_concerned})
    return result