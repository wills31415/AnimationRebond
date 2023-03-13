# coding: utf-8

import pygame
from solar_system import *


# res = (1820, 960)
res = (800, 400)
# res = (200, 100)

middle = (res[0] / 2, res[1] / 2)

soleil = Corps(type = "Star")

pygame.init()
screen = pygame.display.set_mode(res)
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.display.flip()


pygame.quit()
