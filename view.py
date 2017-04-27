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
import pickle
#############################################
# GLOBAL VARIABLES
#############################################
Sprite = namedtuple('Sprite', 'surf x y')
ROAD_COLOR = (150, 115, 33)
BG_COLOR = (70, 204, 63)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 233, 0)
RED = (203, 20, 16)


class View():
    """
    Handles all drawing and interaction which occurs on the screen. Completely decoupled from the
    actual functionality of the car and map, so as to facilitate faster evolution.
    """
    def __init__(self, size=(1000, 1000), map_in=None):
        """
        Initializes window based on size and which map to display. See documentation
        for valid map names.
        """
        self.map_selected, self.autopilot_style = pickle.load(open("map_name.p", "rb"))

        self.track_points = []  # List of mouse points on track
        self.bg_color = (70, 204, 63)  # background color
        self.size = size
        self.world = map_in

        self.screen = pygame.display.set_mode(size)

        self.objs = self.build_obj_canvas()  # list containing all the sprite-objects to be drawn
        self.road_mask = self.get_road_surface(self.world)  # Matrix holding color values

        self.Button1 = Buttons.Button()
        self.coords = (0, 0)

        self.ready_to_draw = False  # Boolean determining if the draw button has been clicked
        self.draw_on = False  # Boolean controlling user drawing on the canvas

    def build_obj_canvas(self, barn_pos=(100, 100), num_corn=100, cow_pos=(150, 150), cow_pos2=(190,100), cow_pos3=(40,80), cow_pos4=(160,50), cow_pos5=(230,150)):
        """
        Creates canvas of all static objects (corn and barn) for faster frame
        updates.
        """
        # Build transparent surface
        obj_surfaces = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32).convert_alpha()
        corn_surf = pygame.image.load("assets/corn.png")  # Load corn image
        barn_surf = pygame.image.load("assets/barn.png")  # Load barn image
        cow_surf = pygame.image.load("assets/cow.png")  # Load cow gif
        cow_surf = pygame.transform.scale(cow_surf, (50, 50))

        all_objs = [Sprite(barn_surf, barn_pos[0], barn_pos[1])]  # Barn object

        all_objs.extend([Sprite(cow_surf, cow_pos[0], cow_pos[1])]) #cow object
        all_objs.extend([Sprite(cow_surf, cow_pos2[0], cow_pos2[1])]) #cow object 2
        all_objs.extend([Sprite(cow_surf, cow_pos3[0], cow_pos3[1])]) #cow object 3
        all_objs.extend([Sprite(cow_surf, cow_pos4[0], cow_pos4[1])]) #cow object 4
        all_objs.extend([Sprite(cow_surf, cow_pos5[0], cow_pos5[1])]) #cow object 5
        # all_objs.extend([obj for obj in [Sprite(cow_surf, randint(-50, 999), randint(0, 999))
                        # for x in range(num_cow)]])

        all_objs.extend([obj for obj in [Sprite(corn_surf, randint(-50, 999), randint(0, 999))
                        for x in range(num_corn)] if self.world.road[obj.x, obj.y] == 0
                        and not (-50 <= obj.x-all_objs[0].x <= 50 and
                                 -50 <= obj.y-all_objs[0].y <= 50)])
        # compiles
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
        self.screen.blit(self.objs, (0, 0))
        if self.map_selected == "None":
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
                # bounds of the upper right button, hacky solution but time was short
                if x > 690 and x < 990 and y > 10 and y < 60:  # If button is pressed and released
                    self.draw_on = False  # Make sure we already aren't drawing
                    self.ready_to_draw = True  # Make it possible to draw
                    world.car.visible = False  # Stop drawing the car temporarily
                    self.road_mask = pygame.Surface((world.road.shape[0], world.road.shape[1]), pygame.SRCALPHA, 32).convert_alpha()

                elif self.draw_on:  # If the mouse was lifted up after drawing
                    self.draw_on = False
                    self.objs = self.build_obj_canvas()  # rebuild sprites to avoid road
                    world.car_start_angle = get_start_angle(world.track_points)
                    world.reset_car()  # Reset the car, the track has been re-drawn
                    world.car.visible = True
                    world.update_checkpoints()
                    self.road_mask = self.get_road_surface(self.world) #rerenders the road picture on the screen so it is clear fo road


            if e.type == pygame.MOUSEMOTION:
                if self.draw_on:
                    world.track_points.append(e.pos)  # adds position of mouse to checkpoint list
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

        mask.blit(rot_surf, (pos[0] - center_point[0], pos[1]-center_point[1]))

    def get_road_surface(self, world):
        """
        Renders the pixels for a road on the frame.
        """
        road = world.road # Load the road
        mask = pygame.Surface((road.shape[0], road.shape[1]), pygame.SRCALPHA, 32).convert_alpha()

        for x in range(0, road.shape[0]):
            for y in range(0, road.shape[1]):
                if road[x, y] == 255:
                    mask.set_at((x, y), ROAD_COLOR)

        self.draw_starting_line(world, mask)
        # TODO Make this less wildly computationally inefficient
        for x in range(0, road.shape[0]):
            for y in range(0, road.shape[1]):
                if road[x, y] != 255:
                    mask.set_at((x, y), BG_COLOR)
        return mask

    def draw_car(self, car):
        """
        Draws the car onto the frame.
        """

        x_pos, y_pos = car.position  # Get car position, angle
        theta = -car.angle[0]  # To account for the switch of angular direction in physics

        car_sprite = pygame.image.load("assets/car.png")  # Load car sprite
        # Scale the car sprite to be the correct size
        car_sprite = pygame.transform.scale(car_sprite, (car.sprite_w, car.sprite_h))
        car_rect = car_sprite.get_rect()  # Get rect for car

        # Rotate the car sprite in place
        rot_car = pygame.transform.rotate(car_sprite, 180-theta*(180/3.1416))
        new_rect = rot_car.get_rect(center=car_rect.center)  # Needed to keep car in same place
        new_rect.topleft = (new_rect.topleft[0] + x_pos, new_rect.topright[1] + y_pos)

        self.draw_lidar(car)
        self.screen.blit(rot_car, new_rect)

    def update_draw_vector(self, car):
        theta = -car.angle[0]
        autopilot_vector = np.matrix([[self.coords[0]], [self.coords[1]]])
        lateral_vector = np.matrix([[self.coords[0]], [0]])
        longitudinal_vector = np.matrix([[0], [self.coords[1]]])

        rotation_matrix = np.matrix([[math.cos(theta), -1 * math.sin(theta)],
                                     [math.sin(theta), math.cos(theta)]])

        position_matrix = np.matrix([[car.position[0]], [car.position[1]]])

        autopilot_vector = rotation_matrix * autopilot_vector + position_matrix
        autopilot_vector = ((int)(autopilot_vector.item(0)), (int)(autopilot_vector.item(1)))

        lateral_vector = rotation_matrix * lateral_vector + position_matrix
        lateral_vector = ((int)(lateral_vector.item(0)), (int)(lateral_vector.item(1)))

        longitudinal_vector = rotation_matrix * longitudinal_vector + position_matrix
        longitudinal_vector = ((int)(longitudinal_vector.item(0)), (int)(longitudinal_vector.item(1)))

        pygame.draw.line(self.screen, (0, 0, 255), (car.position[0]+car.sprite_w/2, car.position[1]+car.sprite_h/2), autopilot_vector)
        pygame.draw.line(self.screen, (255, 255, 0), (car.position[0]+car.sprite_w/2, car.position[1]+car.sprite_h/2), lateral_vector)
        pygame.draw.line(self.screen, (255, 0, 255), autopilot_vector, lateral_vector)

    def draw_lidar(self, car):
        """
        Draws lidar beams
        """
        # NOTE: Enable to draw the car's hitbox in white
        # pygame.draw.polygon(self.screen, WHITE, car.points)

        self.update_draw_vector(car)
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
        """
        #Parameters:                  surface,    color,     x,  y, length, height, width,    text,          text_color
        self.Button1.create_button(self.screen, (107,142,35), 690, 10, 300,    50,    0,  "Draw New Track", (255,255,255))

    def press_button(self, events):
        """
            Defines what happens when button is pressed
        """
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.Button1.pressed(pygame.mouse.get_pos()):
                    self.world.road = np.zeros(self.size)  # when pressed, contents of road matrix is cleared, aka set to 0
                    self.road_mask = self.get_road_surface(self.world)  # re-renders the road picture on the screen so it is clear of road

# http://stackoverflow.com/questions/597369/how-to-create-ms-paint-clone-with-python-and-pygame

    def roundline(self, world, color, start, end, radius):
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

            # Draws the circle on the surface of the road
            pygame.draw.circle(self.road_mask, (150, 115, 33), (x, y), int(radius/2), 0)

        world.road[world.road > 0] = 255  # This fixes issues with LIDAR drawings


# https://github.com/GGRice/InteractiveProgramming/blob/master/pong.py

    def text_objects(self, text, font, color):

        """
           Helper function for draw_start
           Creates font of certain type, size, and color
        """

        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def draw_start(self, size):
        """Creates the classic start screen"""

        #creates new screen, initializes it's colors and creates fonts

        screen1 = pygame.display.set_mode(size)
        screen1.fill(WHITE)

        # Initializes font used in start screen
        pygame.font.init()
        myfont = pygame.font.Font('freesansbold.ttf', 30)
        mymedfont = pygame.font.Font('freesansbold.ttf', 40)
        mylargefont = pygame.font.Font('freesansbold.ttf', 50)

        # Loads assets
        corn_surf = pygame.image.load("assets/corn.png")

        #creates text objects to be printed
        TextSurf, TextRect = self.text_objects('Maize Racer', mylargefont, YELLOW)
        TextSurf1, TextRect1 = self.text_objects('Can you survive the', myfont, YELLOW)
        TextSurf2, TextRect2 = self.text_objects('craziest track of all time...', myfont, YELLOW)
        TextSurf3, TextRect3 = self.text_objects('Only you decide!', mymedfont, YELLOW)
        TextSurf4, TextRect4 = self.text_objects('Create your track now!', mylargefont, YELLOW)
        TextSurf5, TextRect5 = self.text_objects('Press Space Bar to Start', myfont, YELLOW)


        TextSurf6, TextRect6 = self.text_objects('Use the arrow keys to control car!', myfont, YELLOW)
        TextSurf7, TextRect7 = self.text_objects('Go faster using the up arrow,', myfont, YELLOW)
        TextSurf8, TextRect8 = self.text_objects('and slow down using the down arrow.', myfont, YELLOW)
        TextSurf9, TextRect9 = self.text_objects('Steer with the left and right arrows', myfont, YELLOW)
        TextSurf10, TextRect10 = self.text_objects('Draw track by clicking button then drawing with mouse', myfont, YELLOW)
        TextSurf11, TextRect11 = self.text_objects('Draw a track then test your skills!', myfont, YELLOW)

        #determines location for each text in terms of center of screen
        TextRect.center = ((size[0]/2), (size[1]/4 - 100))
        TextRect1.center = ((size[0]/2), (size[1]/2 - 250))
        TextRect2.center = ((size[0]/2), (size[1]/2 - 200))
        TextRect3.center = ((size[0]/2), (size[1]/2 - 150))
        TextRect4.center = ((size[0]/2), (size[1]/2 - 50))
        TextRect5.center = ((size[0]/2), (size[1]/4 * 3.5))
        TextRect6.center = ((size[0]/2), (size[1]/2)+40)
        TextRect7.center = ((size[0]/2), (size[1]/2)+80)
        TextRect8.center = ((size[0]/2), (size[1]/2)+120)
        TextRect9.center = ((size[0]/2), (size[1]/2)+160)
        TextRect10.center = ((size[0]/2), (size[1]/2)+200)
        TextRect11.center = ((size[0]/2), (size[1]/2)+300)

        #actually displays the text on the screen
        screen1.blit(TextSurf, TextRect)
        screen1.blit(TextSurf1, TextRect1)
        screen1.blit(TextSurf2, TextRect2)
        screen1.blit(TextSurf3, TextRect3)
        screen1.blit(TextSurf4, TextRect4)
        screen1.blit(TextSurf5, TextRect5)

        screen1.blit(TextSurf6, TextRect6)
        screen1.blit(TextSurf7, TextRect7)
        screen1.blit(TextSurf8, TextRect8)
        screen1.blit(TextSurf9, TextRect9)
        screen1.blit(TextSurf10, TextRect10)
        screen1.blit(TextSurf11, TextRect11)

        #displays the corn in the 4 corners of the screen

        screen1.blit(corn_surf, (50, 50))
        screen1.blit(corn_surf, (50, size[1]-100))
        screen1.blit(corn_surf, (size[0]-100, 50))
        screen1.blit(corn_surf, (size[0]-100, size[1]-100))

        #updates the display screen
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

# -----------------------------------------------------------------------------
# Run if called from the command line
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    view = View()
    view.draw_scene()
