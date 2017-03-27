import pygame
import numpy as np
from math import sin, cos


class View():
    def __init__(self, map=None):
        self.map = np.round(np.random.rand(1000, 1000))
        self.bg_color = (70, 204, 63)
        self.road_color = (0, 0, 0)
        # self.car = Car()
        # self.objects = []
        self.screen = pygame.display.set_mode((self.map.shape[0], self.map.shape[1]))

    def draw_scene(self):
        """
        Draws one frame of a scene.
        """
        self.screen.fill(self.bg_color)
        self.render_road(self.map)
        self.draw_objects(self.objects)

        pygame.display.flip()

    def render_road(self, road):
        """
        Renders the pixels for a road on the frame.
        """
        for row in range(road.shape[0]):
            for pix in range(road.map.shape[1]):
                if road[row, pix] == 1:
                    self.screen.set_at((row, pix), self.road_color)

    def draw_car(self, car):
        """
        Draws the car onto the frame.
        """
        x, y, theta = car.pos
        w, l = car.size
        vertices = [(x-cos(theta)*w, y+sin(theta)*l), (x+cos(theta)*w, y+sin(theta)*l),
                    (x-cos(theta)*w, y-sin(theta)*l), (x+cos(theta)*w, y-sin(theta)*l)]
        pygame.draw.polygon(self.screen, car.color, vertices)


if __name__ == "__main__":
    View()
