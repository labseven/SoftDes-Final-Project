"""
World:
Holds the map.
"""
from car import Car
import scipy.ndimage as misc
from random import randint
import copy

import numpy as np


class World_Map():
    # CURRENTLY UNUSED
    def __init__(self, size):
        self.world_map = np.zeros(size)
        self.world_map_size = size
        # Quick wall for testing
        for i in range(size[0]):
            self.world_map[i][i] = 1
        print(self.world_map)
        print("Made world_map")


class World():
    def __init__(self, size):
        """
        Initializes the numpy matrix for the road and creates a car.
        """

        self.world_map = World_Map(size)
        self.road = misc.imread('assets/track.png', mode='L')
        self.car = Car(self.road, size, [500, 500], [0, 1], [0.1, 0],
                       car_color=(randint(0, 255),
                                  randint(0, 255),
                                  randint(0, 255)))

        self.order_map = copy.copy(self.road)
        w, h = size
        for c in range(w):
            for r in range(h):
                if self.order_map[r][c] > 0:
                    self.order_map[r][c] = 1
        print(self.order_map)
