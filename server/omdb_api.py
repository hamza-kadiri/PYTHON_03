import requests
from requests import RequestException

# Documentation for the API available at : https://developers.themoviedb.org/3/getting-started/introduction
from omdb_model import SerieEpisode, SerieSeason, Serie, SerieListResults

API_KEY = "84eae13884eb7a9e47fcc760ca08f593"
API_URL = "https://api.themoviedb.org/3"


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


def create_request_exception(method, url, resp):
    resp2 = resp.json()
    return RequestExceptionOMDB(method, url, resp.status_code, resp2['status_message'], resp2['status_code'])


def search_tv_serie_by_title(query: str):
    formatted_query = query.replace(" ", "+")
    url = (API_URL + "/search/tv?api_key={}&query={}".format(API_KEY, formatted_query))
    resp = requests.get(url)
    print(url)
    if resp.status_code != 200:
        raise create_request_exception('GET', url, resp)
    serie_list_results = SerieListResults.from_json(resp.json())
    return serie_list_results


def get_tv_serie(tv_id: int):
    url = API_URL + "/tv/{}?api_key={}".format(tv_id, API_KEY)
    resp = requests.get(url)
    if resp.status_code != 200:
        raise create_request_exception('GET', url, resp)
    serie = Serie.from_json(resp.json())
    return serie


def get_tv_serie_season(tv_id: int, season_number: int):
    url = API_URL + \
        "/tv/{}/season/{}?api_key={}".format(tv_id, season_number, API_KEY)
    resp = requests.get(url)
    if resp.status_code != 200:
        raise create_request_exception('GET', url, resp)
    serie_season = SerieSeason.from_json(resp.json())
    return serie_season


def get_tv_serie_episode(tv_id: int, season_number: int, episode_number: int):
    url = API_URL + "/tv/{}/season/{}/episode/{}?api_key={}".format(tv_id, season_number, episode_number,
                                                                    API_KEY)
    resp = requests.get(url)
    if resp.status_code != 200:
        raise create_request_exception('GET', url, resp)
    serie_episode = SerieEpisode.from_json(resp.json())
    return serie_episode


print(search_tv_serie_by_title("13 Reasons"))
