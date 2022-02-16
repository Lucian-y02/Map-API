import sys

import pygame as pygame

from constants import *
from map import Map
from input import InputStr

pygame.init()

level0_sprites = pygame.sprite.Group()
level1_sprites = pygame.sprite.Group()
level2_sprites = pygame.sprite.Group()
# Добавляем классы
main_map = Map(level0_sprites)
input1 = InputStr(10, 10, 100, 20, level1_sprites)
################################################

pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
FPS = 30

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and pygame.key == pygame.K_ESCAPE):
            running = False

    level0_sprites.update(events)
    level1_sprites.update(events)
    level2_sprites.update(events)

    screen.fill('black')

    level0_sprites.draw(screen)
    level1_sprites.draw(screen)
    level2_sprites.draw(screen)

    if input1.text_out:
        main_map.fstring = input1.text_out
        main_map.remake = True
        main_map.is_moving = False
        input1.text_out = ""
    pygame.display.flip()
    clock.tick(FPS)

sys.exit(pygame.quit())
