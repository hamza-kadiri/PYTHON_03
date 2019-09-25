import requests
from requests import RequestException

# Documentation for the API available at : https://developers.themoviedb.org/3/getting-started/introduction
from server.omdb_model import Episode

API_KEY = "84eae13884eb7a9e47fcc760ca08f593"
API_URL = "https://api.themoviedb.org/3"


class RequestExceptionOMDB(RequestException):
    def __init__(self, method, url, http_status_code, api_status_message, api_status_code):
        RequestException.__init__(self, '{} {} {}'.format(method, url, http_status_code))
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


def create_request_exception(method, url, resp):
    resp2 = resp.json()
    return RequestExceptionOMDB(method, url, resp.status_code, resp2['status_message'], resp2['status_code'])


def search_tv_serie_by_title(query: str):
    # TODO : Format blankspace for query
    url = API_URL + "/search/tv?api_key={}&query={}".format(API_KEY, query)
    resp = requests.get(url)
    if resp.status_code != 200:
        raise create_request_exception('GET', url, resp)
    json = resp.json()
    print(json)


def get_tv_serie(tv_id: int):
    url = API_URL + "/tv/{}?api_key={}".format(tv_id, API_KEY)
    resp = requests.get(url)
    if resp.status_code != 200:
        raise create_request_exception('GET', url, resp)
    json = resp.json()
    print(json)


def get_tv_serie_season(tv_id: int, season_number: int):
    url = API_URL + "/tv/{}/season/{}?api_key={}".format(tv_id, season_number, API_KEY)
    resp = requests.get(url)
    if resp.status_code != 200:
        raise create_request_exception('GET', url, resp)
    json = resp.json()
    print(json)


def get_tv_serie_episode(tv_id: int, season_number: int, episode_number: int):
    url = API_URL + "/tv/{}/season/{}/episode/{}?api_key={}".format(tv_id, season_number, episode_number,
                                                                                API_KEY)
    resp = requests.get(url)
    if resp.status_code != 200:
        raise create_request_exception('GET', url, resp)
    json = Episode.from_json(resp)
    print(json)


get_tv_serie_episode(80865, 1, 1)

