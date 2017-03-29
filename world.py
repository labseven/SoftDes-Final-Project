"""
World:
Holds the map.
"""
from car import Car
import scipy.misc as misc
from random import randint


class World():
    def __init__(self, size):
        """
        Initializes the numpy matrix for the road and creates a car.
        """
        self.road = misc.imread('track.png', mode='L')
        self.car = Car([500, 500], [0, 1], [0, 0], car_color=(randint(0, 255), randint(0, 255), randint(0, 255)))
