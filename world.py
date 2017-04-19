"""
World:
Holds the map.
"""
from car import Car
# import scipy.ndimage as misc
from random import randint
from math import pi
import numpy as np


class World():
    def __init__(self, size=(1000, 1000)):
        """
        Initializes the numpy matrix for the road and creates a car.
        """

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

    def detect_crash(self):
        """
        Returns True if the car has crashed, False otherwise
        """
        hit_points = [self.road[pos] == 0 for pos in self.car.points]
        return any(hit_points)

    def detect_collisions(self):
        """
        Detects whether the car is currently contacting any checkpoints. If it is,
        it removes them from the list of checkpoints
        """
        for checkpoint in self.checkpoints:
            # Difference in positions
            diff_pos = (self.car.position[0]-checkpoint[0], self.car.position[1]-checkpoint[1])
            if (diff_pos[0]**2 + diff_pos[1] ** 2)**(1/2) < 10:  # A checkpoint has been hit
                print("Checkpoint hit!\n")
                self.checkpoints.remove(checkpoint)  # Remove that checkpoint

    def reset_car(self):
        """
        Resets the position, angle, and velocity of the car.
        """
        self.car.position = self.car_start_pos  # Set the car at the starting point
        self.car.angle = [self.car_start_angle, 0]  # Set the car at the starting heading
        self.car.velocity = [0, 0]  # Stop the car

    def update_checkpoints(self, num_checkpoints=3):
        """
        Builds a list of checkpoints based on a list of mouse movement points.
        """
        track_points_len = len(self.track_points)
        checkpoint_indices = [int(track_points_len/(num_checkpoints+1)*val) for val in range(1, num_checkpoints+1)]
        self.checkpoints = [self.track_points[idx] for idx in checkpoint_indices]
