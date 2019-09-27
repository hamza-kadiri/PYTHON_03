import json
from flask import current_app as app

from typing import NamedTuple


class Author:

    @classmethod
    def from_json(cls, json):
        return cls(json['id'], json['name'])

    def __init__(self, id: int, name: str):
        self.__id = id
        self.__name = name

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name


class Network:

    @classmethod
    def from_json(cls, json):
        return cls(json['id'], json['name'])

    def __init__(self, id: int, name: str):
        self.__id = id
        self.__name = name

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name


class Genre:

    @classmethod
    def from_json(cls, json):
        return cls(json['id'], json['name'])

    def __init__(self, id: int, name: str):
        self.__id = id
        self.__name = name

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name


class Crew:

    @classmethod
    def from_json(cls, json):
        return cls(json['id'], json['name'], json['job'])

    def __init__(self, id: int, name: str, job: str):
        self.__id = id
        self.__name = name
        self.__job = job

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def job(self):
        return self.__job


class GuestStar:

    @classmethod
    def from_json(cls, json):
        return cls(json['id'], json['name'], json['character'])

    def __init__(self, id: int, name: str, character: str):
        self.__id = id
        self.__name = name
        self.__character = character

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def character(self):
        return self.__character


class SerieEpisode:

    @classmethod
    def from_json(cls, json):
        return cls(json['id'], json['season_number'], json['episode_number'], json['air_date'], json['overview'],
                   [Crew.from_json(i) for i in json['crew']], [GuestStar.from_json(i) for i in json['guest_stars']])

    def __init__(self, id: int, season_number: int, episode_number: int, air_date: str, overview: str, crew: [Crew],
                 guest_stars: [GuestStar]):
        self.__id = id
        self.__season_number = season_number
        self.__episode_number = episode_number
        self.__air_date = air_date
        self.__overview = overview
        self.__crew = crew
        self.__guest_stars = guest_stars

    def __str__(self):
        return '\r ID : {} \n Season Number : {} \n Episode Number : {} \n Air Date : {} \n Overview : {}' \
            .format(self.__id, self.__season_number, self.__episode_number, self.__air_date, self.__overview)

    @property
    def id(self):
        return self.__id

    @property
    def season_number(self):
        return self.__season_number

    @property
    def episode_number(self):
        return self.__episode_number

    @property
    def air_date(self):
        return self.__air_date

    @property
    def overview(self):
        return self.__overview

    @property
    def crew(self):
        return self.__crew

    @property
    def guest_stars(self):
        return self.__guest_stars


class SerieSeason:

    @classmethod
    def from_json(cls, json):
        return cls(json['id'], json['name'], json['season_number'], json['air_date'], json['overview'],
                   [SerieEpisode.from_json(i) for i in json['episodes']])

    def __init__(self, id: int, name: str, season_number: int, air_date: str, overview: str, episodes: [SerieEpisode]):
        self.__id = id
        self.__name = name
        self.__season_number = season_number
        self.__air_date = air_date
        self.__overview = overview
        self.__episodes = episodes

    def __str__(self):
        return '\r ID : {} \n Name : {} \n Season Number : {} \n Air Date : {} \n Overview : {}' \
            .format(self.__id, self.__name, self.__season_number, self.__air_date, self.__overview)

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def season_number(self):
        return self.__season_number

    @property
    def air_date(self):
        return self.__air_date

    @property
    def overview(self):
        return self.__overview

    @property
    def episodes(self):
        return self.__episodes


class SerieSeasonMini:
    @classmethod
    def from_json(cls, json):
        return cls(json['id'], json['name'], json['season_number'], json['air_date'], json['overview'])

    def __init__(self, id: int, name: str, season_number: int, air_date: str, overview: str):
        self.__id = id
        self.__name = name
        self.__season_number = season_number
        self.__air_date = air_date
        self.__overview = overview

    def __str__(self):
        return '\r ID : {} \n Name : {} \n Season Number : {} \n Air Date : {} \n Overview : {}' \
            .format(self.__id, self.__name, self.__season_number, self.__air_date, self.__overview)

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def season_number(self):
        return self.__season_number

    @property
    def air_date(self):
        return self.__air_date

    @property
    def overview(self):
        return self.__overview


class Serie:

    @classmethod
    def from_json(cls, json):
        return cls(json['id'], json['name'], [Author.from_json(i) for i in json['created_by']], json['first_air_date'],
                   json['last_air_date'], [
                       Genre.from_json(i) for i in json['genres']],
                   [Network.from_json(i) for i in json['networks']],
                   json['number_of_seasons'], json['number_of_episodes'], json['overview'],
                   [SerieSeasonMini.from_json(i) for i in json['seasons']], json['status'])

    def __init__(self, id: int, name: str, created_by: [Author], first_air_date: str, last_air_date: str,
                 genres: [Genre],
                 networks: [Network],
                 number_of_seasons: int, number_of_episodes: int, overview: str, seasons: [SerieSeasonMini],
                 status: str):
        self.__id = id
        self.__name = name
        self.__created_by = created_by
        self.__first_air_date = first_air_date
        self.__last_air_date = last_air_date
        self._genres = genres
        self.__networks = networks
        self.__number_of_seasons = number_of_seasons
        self.__number_of_episodes = number_of_episodes
        self.__overview = overview
        self.__seasons = seasons
        self.__status = status

    def __str__(self):
        return '\r ID : {} \n Name : {} \n First Air Date : {} \n Last Air Date : {} \n Number of seasons : {} \n Number of episodes : {} \n Overview : {} \n Status : {}' \
            .format(self.__id, self.__name, self.__first_air_date, self.__last_air_date, self.__number_of_seasons,
                    self.__number_of_episodes, self.__overview, self.__status)

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def created_by(self):
        return self.__created_by

    @property
    def first_air_date(self):
        return self.__first_air_date

    @property
    def last_air_date(self):
        return self.__last_air_date

    @property
    def genres(self):
        return self._genres

    @property
    def networks(self):
        return self.__networks

    @property
    def number_of_seasons(self):
        return self.__number_of_seasons

    @property
    def number_of_episodes(self):
        return self.__number_of_episodes

    @property
    def overview(self):
        return self.__overview

    @property
    def seasons(self):
        return self.__seasons

    @property
    def status(self):
        return self.__status


class SerieListResult:

    @classmethod
    def from_json(cls, json):
        return cls(json['id'], json['name'], json['first_air_date'], json['overview'], json['backdrop_path'])

    def __init__(self, id: int, name: str, first_air_date: str, overview: str, backdrop_path: str):
        self.__id = id
        self.__name = name
        self.__first_air_date = first_air_date
        self.__overview = overview
        self.__thumbnail_url = f"{app.config['THUMBNAIL_BASE_URL']}{backdrop_path}"

    def __str__(self):
        return '\r ID : {} \n Name : {} \n First Air Date : {} \n Overview : {} \n Thumbnail URL : {}' \
            .format(self.__id, self.__name, self.__first_air_date, self.__overview, self.__thumbnail_url)

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def first_air_date(self):
        return self.__first_air_date

    @property
    def overview(self):
        return self.__overview

    @property
    def thumbnail_url(self):
        return self.__thumbnail_url


class SerieListResults:

    @classmethod
    def from_json(cls, json):
        return cls(json['page'], json['total_pages'], json['total_results'],
                   [SerieListResult.from_json(i) for i in json['results']])

    def __init__(self, page, total_pages, total_results, results: [SerieListResult]):
        self.__page = page
        self.__total_pages = total_pages
        self.__total_results = total_results
        self.__results = results

    def __str__(self):
        return 'Current Page : {}, Total Pages : {}, Total Results : {} \n Results : \n\r {}'.format(self.__page,
                                                                                                     self.__total_pages,
                                                                                                     self.total_results,
                                                                                                     "\n\r >>>>> \n\r".join([str(i) for i in self.__results]))

    def to_dict(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))

    @property
    def page(self):
        return self.__page

    @property
    def total_pages(self):
        return self.__total_pages

    @property
    def total_results(self):
        return self.__total_results

    @property
    def results(self):
        return self.__results
