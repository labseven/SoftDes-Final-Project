"""
@author Matt Brucker
The View class.
"""

import pygame
from pygame.surfarray import blit_array
import numpy as np
from math import sin, cos


class View():
    def __init__(self, size=(1000,1000), map=None):
        self.bg_color = (70, 204, 63)
        self.screen = pygame.display.set_mode(size)

    def draw_scene(self, world):
        """
        Draws one frame of a scene.
        """
        self.screen.fill(self.bg_color)  # Draw background color
        self.render_road(world.road)
        self.draw_car(world.car)
        pygame.display.flip()

    def render_road(self, road):
        """
        Renders the pixels for a road on the frame.
        """
        mask = pygame.Surface((road.shape[0], road.shape[1]))
        blit_array(mask, np.ndarray.astype(road, 'float32'))  # Convert road matrix into pygame surface
        self.screen.blit(mask, (0, 0), None, pygame.BLEND_RGB_ADD)  # Mask road and background together

    def draw_car(self, car):
        """
        Draws the car onto the frame.
        """
        x, y = car.position
        theta = car.angle[0]
        w, l = car.size

        vertices = [(x-l*sin(theta)-w*cos(theta), y+cos(theta)*l-w*sin(theta)),
                    (x-(l*sin(theta))+(w*cos(theta)), y+(cos(theta)*l)+(w*sin(theta))),
                    (x+sin(theta)*l+cos(theta)*w, y-cos(theta)*l+sin(theta)*w),
                    (x+sin(theta)*l-cos(theta)*w, y-cos(theta)*l-sin(theta)*w)]
        pygame.draw.polygon(self.screen, car.color, vertices)  # Draw car
        pygame.draw.polygon(self.screen, (0, 0, 0), vertices, 2)  # Draw outline

        self.draw_lidar(car)

    def draw_lidar(self, car):
        """
        Draws lidar beams.
        """

        for hit in car.lidar_hits:
            pygame.draw.line(self.screen, (250,0,0), car.position, hit)


if __name__ == "__main__":
    view = View()
    view.draw_scene()
