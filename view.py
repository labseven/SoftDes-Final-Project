"""
@author Matt Brucker
The View class.
"""

import pygame
import Buttons
import numpy as np
from random import randint
from collections import namedtuple
import math

Sprite = namedtuple('Sprite', 'surf x y')
ROAD_COLOR = (150, 115, 33)
BG_COLOR = (70, 204, 63)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 233, 0)
RED = (203, 20, 16)


class View():
    def __init__(self, size=(1000, 1000), map_in=None):
        self.track_points = []  # List of mouse points on track
        self.bg_color = (70, 204, 63)

        self.size = size

        self.world = map_in
        self.screen = pygame.display.set_mode(size)
        self.draw_on = False
        self.objs = self.build_obj_canvas()
        self.road_mask = self.get_road_surface(self.world)

        self.Button1 = Buttons.Button()
        self.ready_to_draw = True

        self.order_array_size = 100
        self.order_array = []
        for h in range(self.order_array_size):
            row = []
            for w in range(self.order_array_size):
                row.append(-10)
            self.order_array.append(row)
        self.desirability = 0

    def build_obj_canvas(self, barn_pos=(500, 500), num_corn=100):
        """
        Creates canvas of all static objects (corn and barn) for faster frame
        updates.
        """
        # Build transparent surface
        obj_surfaces = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32).convert_alpha()
        corn_surf = pygame.image.load("assets/corn.png")  # Load corn image
        barn_surf = pygame.image.load("assets/barn.png")  # Load barn image

        all_objs = [Sprite(barn_surf, barn_pos[0], barn_pos[1])]  # Barn object
        all_objs.extend([obj for obj in [Sprite(corn_surf, randint(-50, 999), randint(0, 999))
                        for x in range(num_corn)] if self.world.road[obj.x, obj.y] == 0
                        and not (-50 <= obj.x-all_objs[0].x <= 50 and
                        -50 <= obj.y-all_objs[0].y <= 50)])
        obj_surfaces = self.draw_decorations(all_objs, obj_surfaces)

        return obj_surfaces

    def draw_scene(self, world, events):
        """
        Draws one frame of a scene.
        """
        self.screen.fill(BG_COLOR)  # Draw background color

        radius = 100
        color = (255, 255, 255)

        self.process_draw_events(world, events, radius, color)  # Handle drawing stuff
        self.screen.blit(self.road_mask, (0, 0))  # Mask road and background together
        # self.draw_starting_line(world)
        if world.car.visible:
            self.draw_car(world.car)  # Draw on car
            # for checkpoint in world.checkpoints:
            #     checkpoint_surf = pygame.image.load("assets/checkpoint.png")
            #     self.screen.blit(checkpoint_surf, (checkpoint[0], checkpoint[1]-32))
        self.screen.blit(self.objs, (0, 0))
        self.draw_buttons()
        pygame.display.flip()

    def process_draw_events(self, world, events, radius, color):
        """
        Handles mouse events to decide whether to draw a new track or not, as well as
        car position resetting
        """
        for e in events:  # Iterate through all mouse events
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.ready_to_draw:  # Mouse is pressed and ready to draw
                    world.car_start_pos = (e.pos[0]-world.car.sprite_w/2, e.pos[1]-world.car.sprite_h/2)  # Define new car starting point
                    self.ready_to_draw = False
                    self.draw_on = True

                    world.track_points = [e.pos]

            if e.type == pygame.MOUSEBUTTONUP:
                x, y = e.pos
                if x > 690 and x < 990 and y > 10 and y < 60:  # If button is pressed and released
                    self.draw_on = False  # Make sure we already aren't drawing
                    self.ready_to_draw = True  # Make it possible to draw
                    world.car.visible = False  # Stop drawing the car temporarily
                    self.road_mask = pygame.Surface((world.road.shape[0], world.road.shape[1]), pygame.SRCALPHA, 32).convert_alpha()

                elif self.draw_on:  # If the mouse was lifted up after drawing
                    self.draw_on = False
                    self.objs = self.build_obj_canvas()
                    world.car_start_angle = get_start_angle(world.track_points)
                    world.reset_car()  # Reset the car, the track has been re-drawn
                    world.car.visible = True
                    world.update_checkpoints()
                    self.road_mask = self.get_road_surface(self.world) #rerenders the road picture on the screen so it is clear fo road


            if e.type == pygame.MOUSEMOTION:
                if self.draw_on:
                    world.track_points.append(e.pos)
                    self.roundline(world, color, world.track_points[-1], world.track_points[-2],  radius)  # Draw us some lines

    def draw_starting_line(self, world, mask):
        pos = world.car_start_pos
        angle = -world.car_start_angle
        surf = pygame.image.load("assets/StartingLine.png")

        surf_rect = surf.get_rect()
        rot_surf = pygame.transform.rotate(surf, 180-angle*(180/3.1416))
        center_point = rot_surf.get_rect().center
        # new_rect = rot_surf.get_rect()
        # print(new_rect.center)
        # new_rect.topleft = (new_rect.topleft[0] + pos[0], new_rect.topleft[1] + pos[1])

        mask.blit(rot_surf, (pos[0] -center_point[0], pos[1]-center_point[1]))


    def get_road_surface(self, world):
        """
        Renders the pixels for a road on the frame.
        """
        mask = pygame.Surface((world.road.shape[0], world.road.shape[1]), pygame.SRCALPHA, 32).convert_alpha()

        for x in range(0, world.road.shape[0]):
            for y in range(0, world.road.shape[1]):
                if world.road[x, y] == 255:
                    mask.set_at((x, y), ROAD_COLOR)

        # self.draw_starting_line(world, mask)
        # TODO Make this less wildly computationally inefficient
        for x in range(0, world.road.shape[0]):
            for y in range(0, world.road.shape[1]):
                if world.road[x, y] != 255:
                    mask.set_at((x, y), BG_COLOR)
        return mask


    def draw_car(self, car):
        """
        Draws the car onto the frame.
        """

        x_pos, y_pos = car.position  # Get car position, angle
        theta = -car.angle[0]

        car_sprite = pygame.image.load("assets/car.png")  # Load car sprite
        # Scale the car sprite to be the correct size
        car_sprite = pygame.transform.scale(car_sprite, (car.sprite_w, car.sprite_h))
        car_rect = car_sprite.get_rect()  # Get rect for car

        # Rotate the car sprite in place
        rot_car = pygame.transform.rotate(car_sprite, 180-theta*(180/3.1416))
        new_rect = rot_car.get_rect(center=car_rect.center)  # Needed to keep car in same place
        new_rect.topleft = (new_rect.topleft[0] + x_pos, new_rect.topright[1] + y_pos)

        car.points = [new_rect.topleft, new_rect.topright, new_rect.bottomright, new_rect.bottomleft]

        self.draw_lidar(car)
        self.screen.blit(rot_car, new_rect)


    def draw_lidar(self, car):
        """
        Draws lidar beams.
        """
        for hit in car.lidar_hits:
            pygame.draw.line(self.screen, (250, 0, 0), (car.position[0]+car.sprite_w/2, car.position[1]+car.sprite_h/2), hit)

    def draw_decorations(self, objects, screen):
        """
        Build a surface that contains all of the decorative objects.
        """
        for sprite in objects:
            size = sprite.surf.get_size()
            screen.blit(sprite.surf, (sprite.x-size[0]/2, sprite.y-size[1]))
        return screen

    def draw_buttons(self):
        """
        Creates new button on top right corner of screen
        Parameters:               surface,    color,     x,  y, length, height, width,    text,          text_color
        """
        self.Button1.create_button(self.screen, (107,142,35), 690, 10, 300,    50,    0,  "Draw New Track", (255,255,255))

    def press_button(self, events):
        # Defines what happens when button is pressed
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.Button1.pressed(pygame.mouse.get_pos()):
                    self.world.road = np.zeros(self.size) #when pressed, contents of road matrix is cleared, aka set to 0


    def roundline(self, world, color, start, end, radius):
        self.desirability += .1
        """
        Draws a round line from one point to another and updates the road matrix
        """
        circ_surface = pygame.Surface((radius, radius))
        circ_surface.fill((0, 0, 0))
        # Builds the stencil for drawing the road
        pygame.draw.circle(circ_surface, (255, 255, 255), (int(radius/2), int(radius/2)), int(radius/2), 0)
        # Converts the stencil to a matrix that is usable
        pix_array = pygame.surfarray.pixels_red(circ_surface)
        dx = end[0]-start[0]
        dy = end[1]-start[1]
        distance = max(abs(dx), abs(dy))
        offset = int(radius/2)  # Offset so the drawing is centered around the cursor
        for i in range(distance):  # loop through the line
            x = int(start[0]+float(i)/distance*dx)  # Current position where we're drawing
            y = int(start[1]+float(i)/distance*dy)

            # Get limits of where we're drawing the circle
            left_val = max(0, x-offset)
            right_val = min(world.road.shape[0], x+offset)
            top_val = max(0, y-offset)
            bottom_val = min(world.road.shape[1], y+offset)

            # Updates the road matrix to reflect new drawing
            width = right_val - left_val
            height = bottom_val - top_val
            world.road[left_val:right_val, top_val:bottom_val] += pix_array[:width, :height]
            x_int = (int)(x / 10)
            y_int = (int)(y / 10)
            num = self.order_array[y_int][x_int]
            if num < 0:
                self.order_array[y_int][x_int] = self.desirability
            # Draws the circle on the surface of the road
            pygame.draw.circle(self.road_mask, (150, 115, 33), (x, y), int(radius/2), 0)

        world.road[world.road > 0] = 255  # This fixes weird LIDAR issues (I don't really know why)

    def text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def draw_start(self, size):
        screen1 = pygame.display.set_mode(size)
        screen1.fill(WHITE)
        pygame.font.init()
        myfont = pygame.font.Font('freesansbold.ttf', 30)
        mymedfont = pygame.font.Font('freesansbold.ttf', 40)
        mylargefont = pygame.font.Font('freesansbold.ttf', 50)

        corn_surf = pygame.image.load("assets/corn.png")

        TextSurf, TextRect = self.text_objects('Corn', mylargefont, YELLOW)
        TextSurfH, TextRectH = self.text_objects('HELL', mylargefont, RED)
        TextSurf1, TextRect1 = self.text_objects('Can you survive the', myfont, YELLOW)
        TextSurf2, TextRect2 = self.text_objects('craziest track of all time...', myfont, YELLOW)
        TextSurf3, TextRect3 = self.text_objects('Only you decide!', mymedfont, YELLOW)
        TextSurf4, TextRect4 = self.text_objects('Create your hell now!', mylargefont, YELLOW)
        TextSurf5, TextRect5 = self.text_objects('Press Space Bar to Start', myfont, YELLOW)

        TextRect.center = ((size[0]/2 - 75), (size[1]/4))
        TextRectH.center = ((size[0]/2 + 75), (size[1]/4))
        TextRect1.center = ((size[0]/2), (size[1]/2 - 200))
        TextRect2.center = ((size[0]/2), (size[1]/2 - 150))
        TextRect3.center = ((size[0]/2), (size[1]/2 - 100))
        TextRect4.center = ((size[0]/2), (size[1]/2))
        TextRect5.center = ((size[0]/2), (size[1]/4 * 3))

        screen1.blit(TextSurf, TextRect)
        screen1.blit(TextSurfH, TextRectH)
        screen1.blit(TextSurf1, TextRect1)
        screen1.blit(TextSurf2, TextRect2)
        screen1.blit(TextSurf3, TextRect3)
        screen1.blit(TextSurf4, TextRect4)
        screen1.blit(TextSurf5, TextRect5)

        screen1.blit(corn_surf, (50, 50))
        screen1.blit(corn_surf, (50, size[1]-100))
        screen1.blit(corn_surf, (size[0]-100, 50))
        screen1.blit(corn_surf, (size[0]-100, size[1]-100))

        pygame.display.update()


def get_start_angle(pos_list):
    """
    Takes in a list of mouse positions when drawing the track, and returns a reasonable approximation of the starting
    angle based on the line between the first and fourth points.
    """
    pos_init = pos_list[0]  # Initial position
    try:
        pos_final = pos_list[3]
    except IndexError:
        pos_final = pos_list[-1]  # Avoid index out of bounds errors

    mouse_vel = (pos_final[0] - pos_init[0], pos_init[1] - pos_final[1])  # Flipped Y values because of display/matrix difference
    return math.atan2(mouse_vel[1], mouse_vel[0])-(math.pi/2)


if __name__ == "__main__":
    view = View()
    view.draw_scene()
