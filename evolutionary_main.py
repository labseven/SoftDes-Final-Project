"""
Script which controls the actual functionality of the world.
Is called from the evaluate_driving function within evolution.py

@author Alex Chapman
(c) April 2017

"""
from world import World
from view import View
import pygame
from math import pi, atan
import pickle
import numpy as np

# maximum braking and acceleration forces.
FORCE = -1000
BRAKING = -500
steering_max = pi/4-.1
INCREMENT = pi/4


def main(draw, control, autopilot=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], map_name="None"):
    """
    Parent function of everything the actual simulation does.
    Inputs:
        Draw        whether or not to display the map
        control     whether or not keyboard input will control the simulation.
        autopilot   List of coefficients to be used in the case that control is not desired.
        map_name    string representation of the map to be used. See documentation for valid names.
    """
    # Initializes world and window
    lives = 4

    size = (1000, 1000)
    world = World(size, map_name)
    view = View(size=size, map_in=world)

    keys_pressed = [0, 0, 0, 0]  # The pressed status of the keys
    start = False  # controls appearance of loading screen
    if control:
        start = True
    score = 0
    # Sets car to the correct starting position based on the map
    reset_car(world, map_name)
    view.road_mask = view.get_road_surface(view.world)
    if draw:
        while start:
            events = get_events()

            # Checks to see if the spacebar has been clicked. if so, it exits
            keys = pygame.key.get_pressed()
            keys_down = [idx for idx, val in enumerate(keys) if val == 1]
            event_keys = (pygame.K_SPACE, 0)
            key_states = [int(key in keys_down) for key in event_keys]
            if key_states[0] is 1:
                start = False

            view.draw_start(size)

    while True:

        events = get_events()

        if control:
            # generates a list of each key's pressed status (0=up, 1=pressed)
            # The list is for keys [W, S, A, D]
            keys_pressed = get_input()

            view.coords = (0, 0)
            view.draw_scene(world, events)
            view.press_button(events)

            world.car.driving_force = (keys_pressed[0] * FORCE - keys_pressed[1] * BRAKING)
            world.car.steering = (keys_pressed[2]-keys_pressed[3]) * INCREMENT
            if world.detect_crash():  # If the car has crashed, reset it
                reset_car(world, map_name)
                lives -= 1
                if lives <= 0:
                    return "Run Out Of Lives!"
        else:
            # Of the form (turn, accelerator)
            # Returns the x and y components respectively of the final summed vector.
            d_steer, d_gas = world.car.sensors.calculate_changes(autopilot)

            if draw:
                # draws the map, car and button
                view.coords = (d_steer, d_gas)
                view.draw_scene(world, events)
                view.press_button(events)
                # Experimental Draving of Autopilot Vector
            # Limits the gas applied to be within the constraints of the system
            if d_gas > 1:
                d_gas = 1
            if d_gas < -1:
                d_gas = -1

            # Sets the new turn and acceleration values for the car
            world.car.driving_force = 2.5 * d_gas * FORCE
            world.car.steering = atan(d_steer / d_gas)
            # print(world.car.driving_force, world.car.steering, end='\r')
            # Limits the amount the wheels can be turned

            if world.draw_new is False:
                # gets the score of the car, as well as a boolean for catching cheating behavior.
                hold, position_score = world.car.update_score(world.reward_matrix)
                if hold == -1:
                    # Car went down in value. Happens on either completion of track or circling behavior
                    reset_car(world)
                    if world.car.time_score < 150:  # If car immediately turns around
                        return 0
                    elif position_score <= .01 and world.car.speed_total > 10000:  # if car completes the track
                        # add the speed to incentivize quicker laptimes
                        score += world.car.average_speed
                    return score

                else:  # car didnt go down in value
                    score = hold

                    # constantly checks for circling to reduce downtime in the case of infinite looping
                if world.car.time_score > 60 and position_score < 1:
                    if np.all(world.reward_matrix == 0):  # catches exception of a track being drawn
                        pass
                    else:
                        return 0
                if world.detect_crash():  # If the car has crashed, reset it
                    reset_car(world, map_name)
                    # print(position_score, world.reward_matrix.max(), world.car.time_score)
                    # catches cheating behavior exploiting the circular nature of any drawn track
                    if position_score > 2 and world.car.time_score < 50:
                        score = 0
                    if world.car.time_score > .2:
                        return score

        if world.car.steering > steering_max:
            world.car.steering = steering_max
        elif world.car.steering < -steering_max:
            world.car.steering = -steering_max
        if world.detect_crash():  # If the car has crashed, reset it
            reset_car(world, map_name)
        # Updates the physics of the car
        world.car.update_pos(world.road)


def reset_car(world, map_name="NONE"):
    """
    Reads the world file and gets the starting position and angle for this specific map
    """
    try:
        if map_name != 'None':
            file_add = map_name + '/'
        else:
            file_add = ''
        temp_position, temp_angle = pickle.load(open(str(file_add) + "pos_ang.p", "rb"))

        world.car_start_pos = temp_position
        world.car_start_angle = temp_angle
        # Moves the car to the correct position as well as the right angle.
        world.reset_car()
    except(FileNotFoundError):
        pass


def get_events():
    """
    Handles getting Pygame events.
    """
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:  # If a quit event is received, exit
            pygame.quit()
    return events


def get_input():
    """
    Returns a list of user input values (keys, mouse presses, mouse pos).
    """
    get_events()
    keys = pygame.key.get_pressed()
    keys_down = [idx for idx, val in enumerate(keys) if val == 1]
    # The event values representing the keys pressed
    event_keys = (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)
    # Convert the list of pressed keys to a list of each relevant key's state
    key_states = [int(key in keys_down) for key in event_keys]
    return key_states


def get_mouse_drawing(events):
    """
    Returns the pressed state of the mouse
    """
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN:
            return True  # Mouse was just pressed, return true
    mouse_state = pygame.mouse.get_rel()
    # If mouse is down and being moved, return true
    return bool(pygame.mouse.get_pressed()[0] and (mouse_state[0] != 0 or mouse_state[1] != 0))


if __name__ == "__main__":
    main(True, True)
