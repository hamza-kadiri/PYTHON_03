import json


class JSONSerializable:
    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)


class Crew(JSONSerializable):
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


class GuestStar(JSONSerializable):
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


class Episode(JSONSerializable):
    def __init__(self, id: int, season_number: int, episode_number: int, air_date: str, overview: str, crew: [Crew],
                 guest_stars: [GuestStar]):
        self.__id = id
        self.__season_number = season_number
        self.__episode_number = episode_number
        self.__air_date = air_date
        self.__overview = overview
        self.__crew = crew
        self.__guest_stars = guest_stars

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
