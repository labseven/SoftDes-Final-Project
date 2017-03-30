"""
World:
Holds the map.
"""
from car import Car
import scipy.misc as misc
from random import randint
import numpy as np

class World_Map():
    def __init__(self, size):
        self.world_map = np.zeros(size)
        self.world_map_size = size
        # Quick wall for testing
        for i in range(size[0]):
            self.world_map[i][i] = 1
        print("Made world_map")


class World():
    def __init__(self, size):
        """
        Initializes the numpy matrix for the road and creates a car.
        """
        self.world_map = World_Map(size)
        self.road = misc.imread('track.png', mode='L')
        self.car = Car(self.world_map, [500, 500], [0, 1], [0.1, 0], car_color=(randint(0, 255), randint(0, 255), randint(0, 255)))
