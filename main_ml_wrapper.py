from world import World
from view import View
import pygame
from math import sin, cos

class GameState():
    """ GameSate is a wapper for the game that runs the simulation, but only
    visualizes it if specified. This is to train and run the neural net (NN) on
    the simulation.
    """

    def __init__(self):
        self.size = (1000,1000)
        self.world = World(size)

    def next_frame(self, input_actions):
        """ Progresses the simulation by one frame,
        Returns sensor values, reward value, crash
        """

        # Changes angular velocity based on keys pressed (should be changed to make it accelerate)
        world.car.velocity[0] = -(-input_actions[0]+input_actions[1])*-sin(world.car.angle[0])*100
        world.car.velocity[1] = -(-input_actions[0]+input_actions_actions[1])*cos(world.car.angle[0])*100
        world.car.angle[1] = (input_actions[2]-input_actions[3])

        world.car.update_pos()

        return
