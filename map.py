from io import BytesIO

import pygame
import requests
from PIL import Image

# from constants import *


def image_convertor(b_string):
    image = Image.open(BytesIO(b_string))
    size = image.size
    typ = image.mode
    data = image.tobytes()
    return pygame.image.fromstring(data, size, typ)


class Map(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(Map, self).__init__(*group)
        self.remake = True
        self.image = None
        self.rect = None
        self.zoom = 8
        self.pos = [0, -0]
        self.pos_step = 0.001
        self.spn_step = 10
        self.mode = "sat"
        self.fstring = 'Узбекистан'

    def update(self, events):
        if self.remake:
            self.search()
            self.get_map()

    def change_pos(self, b_string):
        self.image = image_convertor(b_string)
        self.rect = self.image.get_rect()

    def get_map(self):
        api_map = "http://static-maps.yandex.ru/1.x/"
        params = {
            "ll": f"{self.pos[0]},{self.pos[1]}",
            # "spn": f"{self.spn},{self.spn}",
            "l": self.mode,
            "z": self.zoom
        }
        request = requests.get(api_map, params=params)
        if request.status_code == 200:
            self.change_pos(request.content)
        else:
            print(request.status_code)

    def search(self):
        api_map = "http://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.fstring,
            "format": "json"
        }
        request = requests.get(api_map, params=params)
        if request.status_code == 200:
            result = request.json()
            self.pos = list(map(float, result["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]["Point"]["pos"].split()))
        else:
            print(request.status_code)
