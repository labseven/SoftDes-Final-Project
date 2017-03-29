"""
World:
Holds the map.
"""
import numpy as np
from car import Car
import scipy.misc as misc
from math import pi


class World():
    def __init__(self, size):
        self.road = misc.imread('track.png', mode='L')
        self.car = Car((500, 500), pi/3)
