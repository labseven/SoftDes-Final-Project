from world import World
from view import View
import pygame
import numpy as np
from math import sin, cos

class GameState():
    """ GameSate is a wapper for the game that runs the simulation, but only
    visualizes it if specified. This is to train and run the neural net (NN) on
    the simulation.
    """

    def __init__(self):
        self.size = (1000,1000)
        self.world = World(self.size)

    def next_frame(self, input_actions):
        """ Progresses the simulation by one frame,
        Returns sensor values, reward value, crash
        """

        reward = 0
        terminal = False

        # Changes angular velocity based on keys pressed (should be changed to make it accelerate)
        self.world.car.velocity[0] = -(-input_actions[0]+input_actions[1])*-sin(self.world.car.angle[0])*100
        self.world.car.velocity[1] = -(-input_actions[0]+input_actions[1])*cos(self.world.car.angle[0])*100
        self.world.car.angle[1] = (input_actions[2]-input_actions[3])

        self.world.car.update_pos()

        lidar_data = self.world.car.lidar_distances

        reward = self.world.road_reward[int(self.world.car.position[0])][int(self.world.car.position[1])]

        if reward == 0:
            reward = -1
            terminal = True

        print(lidar_data, reward, terminal)

        return lidar_data, reward, terminal
