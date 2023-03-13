# coding: utf-8


import pygame
import time
import random

from ball import *



def random_tuple(a = (0, 0), b = (1, 1)):
    assert isinstance(a, tuple) and isinstance(b, tuple), "Les deux arguments doivent être des tuples. "
    assert len(a) > 0 and len(a) == len(b), "Les deux tuples doivent être de même taille (non nulle). "
    return tuple([a[i] + random.random() * (b[i] - a[i]) for i in range(len(a))])


def ajouter_corde(env, a, b, N, masse = 1, k = 1, epaisseur = 1):
    point = Point(a, 0.3)
    env.add_fixedPoint(point)
    positions = [(a[0] + (i + 1) / N * (b[0] - a[0]), a[1] + (i + 1) / N * (b[1] - a[1])) for i in range(N)]
    balles = [point] + [Ball(p, (0, 0), epaisseur / 2, masse / N) for p in positions]
    for i in range(N):
        bond = Spring(balles[i], balles[i+1], k = k)
        env.add_movable(balles[i+1])
        env.add_bond(bond)



# res = (1820, 960)
res = (1920, 1080)
# res = (200, 100)

pixelsPerUnit = 10

top_left = (0, 0)
top_right = (res[0], 0)
top = (res[0] / 2, 0)
middle = (res[0] / 2, res[1] / 2)

rayon_min = 1
rayon_max = 1
rayon_particule = 1
k = 1000
range_vitesse_x = 10
range_vitesse_y = 10
N = 40
masse = 5


pygame.init()

env = environnement(res, middle, pixelsPerUnit, g, viscositeDynamiqueAir)

# for i in range(N):
#     rayon = rayon_min + random.random() * (rayon_max - rayon_min)
#     balle = Ball(random_tuple((env.limX[0], env.limY[0]), (env.limX[1], env.limY[1])), random_tuple((-range_vitesse_x, -range_vitesse_y), (range_vitesse_x, range_vitesse_y)), rayon, rayon ** 3)
#     env.add_movable(balle)

# point0 = Point((0, 0), 0.3)
# env.add_fixedPoint(point0)
#
# balle1 = Ball((10, 0), (-10, 0), rayon_particule, rayon_particule)
# env.add_movable(balle1)
#
# elastic01 = Elastic(point0, balle1, k = k)
# env.add_bond(elastic01)
#
# balle2 = Ball((20, 0), (0, 0), rayon_particule, rayon_particule)
# env.add_movable(balle2)
#
# spring12 = Spring(balle1, balle2, k = k)
# env.add_bond(spring12)
#
# point3 = Point((30, 0), 0.3)
# env.add_fixedPoint(point3)
#
# elastic23 = Elastic(balle2, point3, k = k)
# env.add_bond(elastic23)

ajouter_corde(env, (0, 0), (20, 0), N, masse, k, 0)

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



    # Flip the display

    pygame.display.flip()


# Done! Time to quit.

pygame.quit()
