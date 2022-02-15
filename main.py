import sys

import pygame as pygame

from constants import *
from map import Map

level0_sprites = pygame.sprite.Group()
level1_sprites = pygame.sprite.Group()
level2_sprites = pygame.sprite.Group()
# Добавляем классы
Map(level0_sprites)
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

    pygame.display.flip()
    clock.tick(FPS)

sys.exit(pygame.quit())
