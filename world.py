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
        self.car = Car(self.road, size, [200, 500], [0, 1], [0.1, 0],
                       car_color=(randint(0, 255),
                                  randint(0, 255),
                                  randint(0, 255)))

        self.car_start_pos = (500, 500)
        self.car_start_angle = 0

        self.order_map = copy.copy(self.road)
        w, h = size
        for c in range(w):
            for r in range(h):
                if self.order_map[r][c] > 0:
                    self.order_map[r][c] = 1
        print(self.order_map)

    def sum_order(self, map_addition):
        print(map_addition.shape)

    def detect_crash(self):
        """
        Returns True if the car has crashed, False otherwise
        """
        car_pos = self.car.position
        return self.road[int(car_pos[0]), int(car_pos[1])] == 0

    def reset_car(self):
        """
        Resets the position, angle, and velocity of the car.
        """
        self.car.position = self.car_start_pos  # Set the car at the starting point
        self.car.angle = [self.car_start_angle, 0]  # Set the car at the starting heading
        self.car.velocity = [0, 0]  # Stop the car
