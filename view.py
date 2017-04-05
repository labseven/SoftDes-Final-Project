"""
@author Matt Brucker
The View class.
"""

import pygame
from pygame.surfarray import blit_array
import numpy as np
from math import cos
from random import randint


class View():
    def __init__(self, size=(1000, 1000), map_in=None):
        self.bg_color = (70, 204, 63)
        self.screen = pygame.display.set_mode(size)
        self.world = map_in
        self.objs = self.build_obj_canvas()


    def build_obj_canvas(self):
        objects = [("assets/corn.png", randint(0, 999), randint(0, 999)) for x in range(5000)]
        barn = [("assets/barn.png", randint(0, 900), randint(0, 900))]
        obj_surfaces = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32).convert_alpha()
        valid_objects = [obj for obj in objects if self.world.road[obj[1], obj[2]] == 0]
        obj_surfaces = self.draw_decorations(valid_objects, obj_surfaces)
        obj_surfaces = self.draw_decorations(barn, obj_surfaces)

        return obj_surfaces

    def draw_scene(self, world):
        """
        Draws one frame of a scene.
        """
        self.screen.fill(self.bg_color)  # Draw background color
        self.render_road(self.world.road)
        self.screen.blit(self.objs, (0, 0))
        self.draw_car(self.world.car)
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
        x_pos, y_pos = car.position
        theta = car.angle[0]

        car_sprite = pygame.image.load("assets/car.png")
        car_rect = car_sprite.get_rect(center=(16, 32))

        rot_car = pygame.transform.rotate(car_sprite, 180-theta*(180/3.1416))
        new_rect = rot_car.get_rect(center=car_rect.center)
        new_rect.topleft = (new_rect.topleft[0] + x_pos, new_rect.topright[1] + y_pos)

        self.screen.blit(rot_car, new_rect)
        self.draw_lidar(car)

    def draw_lidar(self, car):
        """
        Draws lidar beams.
        """

        for hit in car.lidar_hits:
            pygame.draw.line(self.screen, (250, 0, 0), (car.position[0]+16, car.position[1]+32), hit)

    def draw_decorations(self, objects, screen):
        for obj in objects:
            img_sprite = pygame.image.load(obj[0])
            screen.blit(img_sprite, (obj[1], obj[2]))
        return screen


if __name__ == "__main__":
    view = View()
    view.draw_scene()
