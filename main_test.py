# coding: utf-8


import pygame
import time
import random

from ball import *



def random_tuple(a = (0, 0), b = (1, 1)):
    assert isinstance(a, tuple) and isinstance(b, tuple), "Les deux arguments doivent être des tuples. "
    assert len(a) > 0 and len(a) == len(b), "Les deux tuples doivent être de même taille (non nulle). "
    return tuple([a[i] + random.random() * (b[i] - a[i]) for i in range(len(a))])



# res = (1820, 960)
res = (800, 400)

pixelsPerUnit = 5

top_left = (0, 0)
top_right = (res[0], 0)
top = (res[0] / 2, 0)
middle = (res[0] / 2, res[1] / 2)

rayon1 = 2
rayon2 = 2
range_vitesse_x = 0
range_vitesse_y = 0


pygame.init()

env = environnement(res, middle, pixelsPerUnit)

point0 = Point((0, 0), 0.3)
env.add_fixedPoint(point0)

balle1 = Ball((10, 0), (0, 0), rayon1, rayon1 ** 3)
env.add_movable(balle1)

balle2 = Ball((20, 0), (0, 0), rayon2, rayon2 ** 3)
env.add_movable(balle2)

rod01 = Rod(point0, balle1)
env.add_bond(rod01)

rod12 = Rod(balle1, balle2)
env.add_bond(rod12)


# Set up the drawing window

screen = pygame.display.set_mode(res)


# Run until the user asks to quit

running = True

# ______BOUCLE_____
while running:

    env.update_env()
    # Did the user click the window close button?

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


    # Fill the background with white

    screen.fill((255, 255, 255))


    # Draw all the bonds in black
    for bond in env.bonds:
        pygame.draw.line(screen, (0, 0, 0), env.locate(bond.point1.position), env.locate(bond.point2.position), bond.epaisseur)

    # Draw all the fixed objects in red
    for point in env.fixedPoints:
        pygame.draw.circle(screen, (255, 0, 0), env.locate(point.position), point.rayon * env.pixelsPerUnit)

    # Draw all the movable objects in blue
    for movable in env.movables:
        pygame.draw.circle(screen, (0, 0, 255), env.locate(movable.position), movable.rayon * env.pixelsPerUnit)

    # time.sleep(dt)
    print(Point.dist(point0, balle1), Point.dist(balle1, balle2))



    # Flip the display

    pygame.display.flip()


# Done! Time to quit.

pygame.quit()




"""
    creation de la fenetre
"""
