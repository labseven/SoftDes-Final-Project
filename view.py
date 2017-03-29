import pygame
import numpy as np
from math import sin, cos
from car import *


class View():
    def __init__(self, map=None):
        self.bg_color = (70, 204, 63)
        self.road_color = (0, 0, 0)
        # self.objects = []
        self.screen = pygame.display.set_mode((1000,1000))

    def draw_scene(self, world):
        """
        Draws one frame of a scene.
        """
        while True:
            self.screen.fill(self.bg_color)
            self.render_road(world.road)
            self.draw_car(world.car)
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
        w, l = (50, 100)
        vertices = [(x+l*sin(theta)+w*cos(theta), y+cos(theta)*l-w*sin(theta)), (x+(l*sin(theta))-(w*cos(theta)), y+(cos(theta)*l)+(w*sin(theta))),
                    (x+sin(theta)*l+cos(theta)*w, y-cos(theta)*l+sin(theta)*w), (x+sin(theta)*l-cos(theta)*w, y-cos(theta)*l-sin(theta)*w)]
        pygame.draw.polygon(self.screen, (128,128,128), vertices)


if __name__ == "__main__":
    view = View()
    view.draw_scene()
