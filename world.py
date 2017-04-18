"""
World:
Holds the map.
"""
from car import Car
# import scipy.ndimage as misc
from random import randint
from math import pi

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
    def __init__(self, size=(1000, 1000)):
        """
        Initializes the numpy matrix for the road and creates a car.
        """

        # self.road = World_Map(size)
        self.size = size
        self.road = np.zeros(size)
        self.track_points = []
        # self.road = misc.imread('assets/track.png', mode='L')
        self.car = Car(self.road, size, [200, 500], [0, 1], [0.1, 0],
                       car_color=(randint(0, 255),
                                  randint(0, 255),
                                  randint(0, 255)))

        self.car_start_pos = (500, 500)
        self.car_start_angle = 0

        self.order_map = self.road.copy()
        w, h = size
        for c in range(w):
            for r in range(h):
                if self.order_map[r][c] > 0:
                    self.order_map[r][c] = 1

        self.checkpoints = []

        self.reward_matrix = np.zeros(size)

    def detect_crash(self):
        """
        Returns True if the car has crashed, False otherwise
        """
        if np.all(self.reward_matrix == 0):
            return False
        else:
            try:
                hit_points = [self.road[pos] == 0 for pos in self.car.points]
                return any(hit_points)
            except:
                return True

    def reset_car(self):
        """
        Resets the position, angle, and velocity of the car.
        """
        self.car.position = self.car_start_pos  # Set the car at the starting point
        self.car.angle = [self.car_start_angle, 0]  # Set the car at the starting heading
        self.car.velocity = [0, 0]  # Stop the car

    def update_checkpoints(self, num_checkpoints=100):
        track_points_len = len(self.track_points)
        checkpoint_indices = [int(track_points_len/(num_checkpoints+1)*val) for val in range(1, num_checkpoints+1)]
        self.checkpoints = [self.track_points[idx] for idx in checkpoint_indices]
        self.update_reward_matrix()

    def update_reward_matrix(self):
        checks = len(self.checkpoints)
        for value, checkpoint in enumerate(self.checkpoints):
            radius = 50
            print('Rendering Reward Matrix:', (int)((value/checks)*10000) / 100, 'Percent Complete', end='\r')
            for y, row in enumerate(self.reward_matrix):
                for x, rand in enumerate(row):
                    x_dist = abs(x - checkpoint[0])
                    y_dist = abs(y - checkpoint[1])
                    if x_dist < radius and y_dist < radius:
                        self.reward_matrix[y][x] = value / 10
        print(end='\r')
