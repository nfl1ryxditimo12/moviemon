from django.shortcuts import resolve_url
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
        f =  open("save_game/save_game.bin", "wb") 
        pickle.dump(data, f)
        f.close()
        return data
    except:
        return None

def load_session_data():
    try:
        f = open("save_game/save_game.bin", "rb")
        data = pickle.load(f)
        f.close()
        return data
    except:
        return None

def valid_movie_list(movie_list, result):
    low = 0
    high = 0
    for id in movie_list:
        if result.moviemon[id].rating < 4:
            low += 1
        elif result.moviemon[id].rating >= 7:
            high += 1
    if low < 3 or high < 3:
        return False
    return True

def get_movie_list(movie_list):
    result = GameData()
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
    if not valid_movie_list(movie_list, result):
        return get_movie_list(movie_list)
    return result

def get_init_map(movie_list):
    map = [[0 for col in range(10)] for row in range(10)]
    
    for i in range(0, 10):
        for j in range(0, 10):
            map[i][j] = random.choice(['ground', 'ground', 'ground', random.choice(['ball', str(random.sample(movie_list, len(movie_list)))])])
    map[5][5] = 'player'
    
    return map



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

    def __str__(self):
        return str({
            "title": self.title,
            "year": self.year,
            "director": self.director,
            "poster": self.poster,
            "rating": self.rating,
            "plot": self.plot,
            "actors": self.actors,
        })

class GameData:
    def __init__(self) -> None:
        self.pos: dict = settings.PLAYER_COORDINATE
        self.ball_count: int = settings.MOVIE_BALL_COUNT
        self.captured_list: List(str) = []
        self.moviemon: Dict[str, Moviemon] = {}

        # 수정 필요
        self.map: List[List] = []

    def get_random_movie(self):
        id = [m for m in self.moviemon.keys() if not m in self.captured_list]
        return random.choice(id)

    def get_strength(self):
        pass

    def get_movie(self, movimon_id):
        return self.moviemon[movimon_id]

    def dump(self):
        return {
            'pos': self.pos,
            'ball_count': self.ball_count,
            'captured_list': self.captured_list,
            'moviemon': self.moviemon,
            'map': self.map
        }

    @staticmethod
    def load(data):
        result = GameData()
        result.pos = data["pos"]
        result.moviemon = data['moviemon']
        result.ball_count = data['ball_count']
        result.captured_list = data['captured_list']
        result.map = data['map']
        return result    

    
    @staticmethod
    def load_default_settings():
        movie_list = random.choice([settings.MOVIE_LIST, settings.MOVIE_LIST_KOR])

        # 나중에 사용할 영화 리스트 변수
        # result = get_movie_list(movie_list)

        # 로컬에 영화 리스트 저장 후 사용하는 코드
        result = GameData()
        f = open('save_game/movie_list.bin', 'rb')
        data = dict(pickle.load(f))
        f.close()
        for id in movie_list:
            for key, value in data.items():
                if id == key:
                    result.moviemon[id] = value
        
        result.map = get_init_map(movie_list)
        return result
        