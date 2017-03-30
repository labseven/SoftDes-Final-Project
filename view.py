import pygame
import numpy as np
import scipy.misc as misc
from math import sin, cos
from car import *


class View():
    def __init__(self, size=(1000,1000), map=None):
        self.road = misc.imread('track.png', mode='L')
        self.bg_color = (70, 204, 63)
        self.road_color = (0, 0, 0)
        self.car = Car((500.1,500.75), 0)
        # self.objects = []
        self.screen = pygame.display.set_mode(size)

    def draw_scene(self):
        """
        Draws one frame of a scene.
        """

        self.screen.fill(self.bg_color)
        self.render_road(self.road)
        self.draw_car(self.car)
        # self.draw_objects(self.objects)
        pygame.display.flip()

    def render_road(self, road):
        """
        Renders the pixels for a road on the frame.
        """
        for row in range(road.shape[0]):
            for pix in range(road.shape[1]):
                if road[row, pix] > 0:
                    self.screen.set_at((row, pix), self.road_color)

    def draw_car(self, car):
        """
        Draws the car onto the frame.
        """
        x, y = car.position
        theta = car.angle
        w, l = car.size
        vertices = [(x-cos(theta)*w, y+sin(theta)*l), (x+cos(theta)*w, y+sin(theta)*l),
                    (x-cos(theta)*w, y-sin(theta)*l), (x+cos(theta)*w, y-sin(theta)*l)]
        # print(vertices)
        pygame.draw.polygon(self.screen, car.color, vertices)


if __name__ == "__main__":
    view = View()
    view.draw_scene()
