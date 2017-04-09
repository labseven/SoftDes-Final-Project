"""
@author Matt Brucker
The View class.
"""

import pygame
from random import randint
from collections import namedtuple
import numpy as np

Sprite = namedtuple('Sprite', 'surf x y')

class View():
    def __init__(self, size=(1000, 1000), map_in=None):
        self.bg_color = (70, 204, 63)

        self.screen = pygame.display.set_mode(size)
        self.world = map_in
        self.draw_on = False
        self.last_pos = (0, 0)
        self.objs = self.build_obj_canvas()
        self.road_mask = self.get_road_surface(self.world.road)


    def build_obj_canvas(self):
        # Build transparent surface
        obj_surfaces = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32).convert_alpha()
        corn_surf = pygame.image.load("assets/corn.png") # Load corn image
        barn_surf = pygame.image.load("assets/barn.png") # Load barn image

        all_objs = [Sprite(barn_surf, 500, 500)]
        all_objs.extend([obj for obj in [Sprite(corn_surf, randint(-50, 999), randint(0, 999))
                        for x in range(5000)] if self.world.road[obj.x, obj.y] == 0
                        and not (-50 <= obj.x-all_objs[0].x <= 50 and
                        -50 <= obj.y-all_objs[0].y <= 50)])
        obj_surfaces = self.draw_decorations(all_objs, obj_surfaces)

        return obj_surfaces


    def draw_scene(self, world, events):
        """
        Draws one frame of a scene.
        """
        self.screen.fill(self.bg_color)  # Draw background color

        radius = 100
        color = (255, 255, 255)
        for e in events:
            if e.type == pygame.QUIT:
                raise StopIteration
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.roundline(world, color, e, e.pos,  radius)
                self.draw_on = True
            if e.type == pygame.MOUSEBUTTONUP:
                # self.road_mask = self.get_road_surface(self.world.road)
                self.objs = self.build_obj_canvas()
                self.draw_on = False
            if e.type == pygame.MOUSEMOTION:
                if self.draw_on:
                    # world.road[e.pos[0]:e.pos[0]+10, e.pos[1]:e.pos[1]+10] = 255
                    # pygame.draw.rect(self.road_mask, (150, 115, 33), (e.pos[0], e.pos[1], radius, radius), 0)
                    self.roundline(world, color, e, self.last_pos,  radius)
                self.last_pos = e.pos

        self.screen.blit(self.road_mask, (0, 0))  # Mask road and background together
        self.screen.blit(self.objs, (0, 0))
        self.draw_car(self.world.car)

        pygame.display.flip()

    def get_road_surface(self, road):
        """
        Renders the pixels for a road on the frame.
        """
        mask = pygame.Surface((road.shape[0], road.shape[1]), pygame.SRCALPHA, 32).convert_alpha()

        for x in range(0, road.shape[0]):
            for y in range(0, road.shape[1]):
                if road[x,y] > 0:
                    mask.set_at((x, y), (150, 115, 33))
        return mask

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
        """
        Build a surface that contains all of the decorative objects.
        """
        for sprite in objects:
            size = sprite.surf.get_size()
            screen.blit(sprite.surf, (sprite.x-size[0]/2, sprite.y-size[1]))
        return screen

    def roundline(self, world, color, e, end, radius):
        circ_surface = pygame.Surface((100, 100))
        circ_surface.fill((0, 0, 0))
        pygame.draw.circle(circ_surface, (255, 255, 255), (int(radius/2), int(radius/2)), int(radius/2), 0)

        pix_array = pygame.surfarray.pixels_red(circ_surface)

        print(pix_array)
        start = e.pos
        dx = end[0]-start[0]
        dy = end[1]-start[1]
        distance = max(abs(dx), abs(dy))

        offset = int(radius/2)
        for i in range(distance):
            x = int(start[0]+float(i)/distance*dx)
            y = int(start[1]+float(i)/distance*dy)

            world.road[x-offset:x+offset, y-offset:y+offset] += pix_array
            # world.road[x-offset:x+offset, y-offset:y+offset] = np.clip(world.road[x-offset:x+offset, y-offset:y+offset], 0, 255)
            pygame.draw.circle(self.road_mask, (150, 115, 33), (x, y), int(radius/2), 0)


if __name__ == "__main__":
    view = View()
    view.draw_scene()
