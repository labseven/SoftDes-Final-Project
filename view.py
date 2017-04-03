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
        self.draw_on = False
        self.last_pos = (0, 0)
        self.draw_on = False
        self.last_pos = (0, 0)


    def draw_scene(self, world):
        """
        Draws one frame of a scene.
        """
        self.screen.fill(self.bg_color)  # Draw background color
        self.render_road(world.road)

        radius = 100
        color = (255, 255, 255)
        e = pygame.event.wait()
        if e.type == pygame.QUIT:
            raise StopIteration
        if e.type == pygame.MOUSEBUTTONDOWN:
            world.road[e.pos[0]:e.pos[0]+radius, e.pos[1]:e.pos[1]+radius] = 255
            self.draw_on = True
        if e.type == pygame.MOUSEBUTTONUP:
            self.draw_on = False
        if e.type == pygame.MOUSEMOTION:
            if self.draw_on:
                world.road[e.pos[0]:e.pos[0]+10, e.pos[1]:e.pos[1]+10] = 255
                self.roundline(world, color, e, self.last_pos,  radius)
            self.last_pos = e.pos

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

    def roundline(self, world, color, e, end, radius):
        start = e.pos
        dx = end[0]-start[0]
        dy = end[1]-start[1]
        distance = max(abs(dx), abs(dy))
        for i in range(distance):
            x = int( start[0]+float(i)/distance*dx)
            y = int( start[1]+float(i)/distance*dy)
            world.road[x:x+radius, y:y+radius] = 255
<<<<<<< HEAD

=======
>>>>>>> 28f48b3f8cc2a671f255108804fed66e5c8bb6ed

if __name__ == "__main__":
    view = View()
    view.draw_scene()
