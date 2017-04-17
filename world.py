"""
World:
Holds the map.
"""
from car import Car
import scipy.ndimage as misc
from random import randint
from math import pi

import numpy as np

class World():
    def __init__(self, size):
        """
        Initializes the numpy matrix for the road and creates a car.
        """

        self.road = misc.imread('assets/track.png', mode='L')
        self.road[100][100] = 1
        self.road_reward = self.make_road_reward(self.road)
        self.car = Car(self.road, size, [750, 750], [-1, 1], [0.1, 0], car_color=(randint(0, 255), randint(0, 255), randint(0, 255)))

    def make_road_reward(self, road):
        road_reward = np.copy(road)

        # Find start position
        for x in range(road_reward.shape[0]):
            for y in range(road_reward.shape[1]):
                if road_reward[x][y] == 1:
                    start_loc_x, start_loc_y = x,y
                    break

        print(start_loc_x, start_loc_y)
        self.increment_flood_fill(start_loc_x, start_loc_y, road_reward, 1)
        print(road_reward)

        return road_reward

    def increment_flood_fill(self, loc_x, loc_y, road_reward, value):
        if road_reward[loc_x][loc_y] == 255:
            road_reward[loc_x][loc_y] = value

            value = value + 1
            self.increment_flood_fill(loc_x + 1, loc_y + 1, road_reward, value)
            self.increment_flood_fill(loc_x - 1, loc_y + 1, road_reward, value)
            self.increment_flood_fill(loc_x + 1, loc_y - 1, road_reward, value)
            self.increment_flood_fill(loc_x - 1, loc_y - 1, road_reward, value)
