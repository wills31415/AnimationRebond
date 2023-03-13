#coding: utf-8

import pygame


class Color:
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)


class Point:

    def __init__(self, pos = (0, 0)):
        if not isinstance(pos, tuple):
            raise TypeError("'pos' must be a tuple... ")
        if len(pos) != 2:
            raise TypeError("'pos' must have 2 components... ")

        self._pos = pos



class Canvas:

    def __init__(self):
        points = {}

    def add(self, object):
        pass
