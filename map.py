from io import BytesIO

import pygame
import requests
from PIL import Image


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
        self.zoom = 9
        self.pos = [0, -0]
        self.pos_step = 0.001
        self.spn_step = 10
        self.mode = "sat"
        self.fstring = 'Белая Холуница'
        self.is_moving = False

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    self.zoom = max(1, self.zoom - 1)
                    self.remake = True
                elif event.key == pygame.K_PAGEDOWN:
                    self.zoom = min(18, self.zoom + 1)
                    self.remake = True

                # Перемещение по карте с помощью стрелок
                if event.key == pygame.K_UP:
                    self.pos[1] += self.pos_step
                    self.get_map()
                    self.is_moving = True
                    print(self.pos)
                if event.key == pygame.K_DOWN:
                    self.pos[1] -= self.pos_step
                    self.get_map()
                    self.is_moving = True
                    print(self.pos)
                if event.key == pygame.K_LEFT:
                    self.pos[0] -= self.pos_step
                    self.get_map()
                    self.is_moving = True
                    print(self.pos)
                if event.key == pygame.K_RIGHT:
                    self.pos[0] += self.pos_step
                    self.get_map()
                    self.is_moving = True
                    print(self.pos)
        try:
            if self.remake:
                self.search()
                self.get_map()
                self.remake = False
        except Exception:
            print("Объект не найден!")
            self.remake = False

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

        # Изменение pos_stem взамисимости от zoom
        if 1 <= self.zoom <= 5:
            self.pos_step = 3
        elif 6 <= self.zoom <= 9:
            self.pos_step = 0.1
        elif 10 <= self.zoom <= 12:
            self.pos_step = 0.01
        elif 13 <= self.zoom <= 16:
            self.pos_step = 0.001
        elif 17 <= self.zoom <= 18:
            self.pos_step = 0.0001

    def search(self):
        api_map = "http://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.fstring,
            "format": "json"
        }
        request = requests.get(api_map, params=params)
        if request.status_code == 200 and not self.is_moving:
            result = request.json()
            self.pos = list(map(float, result["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]["Point"]["pos"].split()))
        elif not self.is_moving:
            print(request.status_code)
