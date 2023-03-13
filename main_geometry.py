#coding: utf-8

import pygame
from geometry import *


defaultResolution = (800, 400)

pygame.init()
screen = pygame.display.set_mode(defaultResolution, pygame.RESIZABLE)
# screen = pygame.display.get_surface()

# cursor = pygame.cursors.compile(pygame.cursors.textmarker_strings)
# pygame.mouse.set_cursor((8, 16), (0, 0), *cursor)
# pygame.mouse.set_cursor(*pygame.cursors.diamond)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # print("Mouse position :", pygame.mouse.get_pos())
    # print("Mouse movement :", pygame.mouse.get_rel())
    print("Pressed buttons :", pygame.mouse.get_pressed()[::2])


    screen.fill(Color.white)

    pygame.display.flip()

pygame.quit()
