from rush00.settings import API_KEY
from django.conf import settings

from typing import List, Dict, Tuple

import os
import pickle
import random
import requests

def make_session_dir():
    if not os.path.exists("save_game"):
        os.makedirs("save_game")

def save_session_data(data):
    make_session_dir()
    try:
        with open("save_game/save_game.bin", "wb") as f:   
            pickle.dump(data, f)
        return data
    except:
        return None

def load_session_data(data):
    try:
        with open("save_game/save_game.bin", "rb") as f:   
            data = pickle.load(f)
        return data
    except:
        return None

class Moviemon:
    def __init__(
        self,
        title=None,
        poster=None,
        director=None,
        year=None,
        rating=None,
        plot=None,
        actors=None) -> None:

        self.title = title
        self.poster = poster
        self.director = director
        self.year = year
        self.rating = rating
        self.plot = plot
        self.actors = actors

    def __str__(self) -> str:
        return {
            "title": self.title,
            "year": self.year,
            "director": self.director,
            "poster": self.poster,
            "rating": self.rating,
            "plot": self.plot,
            "actors": self.actors,
        }

class GameData:
    def __init__(self) -> None:
        self.pos: tuple(int, int) = settings.PLAYER_COORDINATE
        self.ball_count: int = settings.MOVIE_BALL_COUNT
        self.captured_list: List(str) = []
        self.moviemon: Dict[str, Moviemon] = {}

        # 수정 필요
        self.map: List[List] = []

    def get_random_movie(self):
        pass

    def get_strength(self):
        pass

    def get_movie(self, movimon_id):
        return self.moviemon[movimon_id]

    def dump(self):
        return {
            'pos': self.pos,
            'ball_count': self.ball_count,
            'captured_list': self.captured_list,
            'map': self.map
        }

    @staticmethod
    def load(data):
        pass

    @staticmethod
    def load_default_settings():
        result = GameData()
        movie_list = random.choice([settings.MOVIE_LIST, settings.MOVIE_LIST_KOR])
        for id in movie_list:
            try:
                URL = "https://www.omdbapi.com/?apikey={api}&i={id}".format(api=API_KEY, id=id)
                data = requests.get(URL).json()
                result.moviemon[id] = Moviemon(
                    data['Title'],
                    data['Poster'],
                    data['Director'],
                    data['Year'],
                    float(data['imdbRating']),
                    data['Plot'],
                    data['Actors']
                )
            except Exception as e:
                assert e
        return result
