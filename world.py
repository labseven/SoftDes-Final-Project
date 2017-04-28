"""
World:
Holds the map.
"""
from car import Car
# import scipy.ndimage as misc
from random import randint
import pickle
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
    def __init__(self, size=(1000, 1000), map_name='NONE'):
        """
        Initializes the numpy matrix for the road and creates a car.
        """
        self.started = False

        # self.road = World_Map(size)
        self.size = size
        self.road = np.zeros(size)
        self.track_points = []
        # self.road = misc.imread('assets/track.png', mode='L')
        self.car_start_pos = (500, 500)
        self.car_start_angle = 0

        map_selected, autopilot_style = pickle.load(open("map_name.p", "rb"))
        if autopilot_style == "3":
            self.draw_new = False
        else:
            self.draw_new = True
            """
        self.reward_matrix = np.zeros(size)
        self.reward_matrix[self.reward_matrix == 0] = -1"""
        try:
            # print('Updated Road and reward files')
            if map_name != 'None':
                file_add = map_name + '/'
            else:
                file_add = ''
            self.road = pickle.load(open(file_add + "road.p", "rb"))
            self.car_start_position, self.car_start_angle = pickle.load(open(file_add + "pos_ang.p", "rb"))
            self.started = True
            self.reward_matrix = pickle.load(open(file_add + "reward.p", "rb"))
        except:
            print(file_add + "pos_ang.p")
            print('Pickle Files Not Found.')

        self.car = Car(self.road, size, [200, 500], [0, 1], [0.1, 0],
                       car_color=(randint(0, 255),
                                  randint(0, 255),
                                  randint(0, 255)))

        self.checkpoints = []

    def detect_crash(self):
        """
        Returns True if the car has crashed, False otherwise
        """
        # print('test', np.all(self.reward_matrix == 0), self.reward_matrix)
        # print('started:', self.started)
        if self.started is False:
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
        self.car.visible = True

    def update_checkpoints(self, num_checkpoints=100):
        """
        Builds a list of checkpoints based on a list of mouse movement points.
        """
        track_points_len = len(self.track_points)
        checkpoint_indices = [int(track_points_len/(num_checkpoints+1)*val) for val in range(1, num_checkpoints+1)]
        self.checkpoints = [self.track_points[idx] for idx in checkpoint_indices]

        combined_save = [self.car_start_pos, self.car_start_angle]

        pickle.dump(self.road, open('road.p', 'wb'))
        pickle.dump(combined_save, open('pos_ang.p', 'wb'))
        self.started = True
        if self.draw_new is True:
                self.update_reward_matrix()
                pickle.dump(self.reward_matrix, open('reward.p', 'wb'))

    def update_reward_matrix(self):
        checks = len(self.checkpoints)
        for value, checkpoint in enumerate(self.checkpoints):
            c_value = (value + .1) / 10
            radius = 50
            print('Rendering Reward Matrix:', (int)((value/checks)*10000) / 100, 'Percent Complete', end='\r')
            for y, row in enumerate(self.reward_matrix):
                for x, rand in enumerate(row):
                    x_dist = abs(x - checkpoint[0])
                    y_dist = abs(y - checkpoint[1])
                    if x_dist < radius and y_dist < radius and rand == 0:
                        self.reward_matrix[y][x] = c_value
        print('                                                         ', end='\r')
