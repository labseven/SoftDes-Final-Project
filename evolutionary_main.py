from world import World
from view import View
import pygame
from math import pi, atan
import pickle
import numpy as np

FORCE = -1000
BRAKING = -500
steering_max = pi/4-.1
INCREMENT = pi/4


def main(draw, control, autopilot=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], map_name="None"):
    # print(autopilot)
    size = (1000, 1000)
    world = World(size, map_name)

    view = View(size=size, map_in=world)

    clock = pygame.time.Clock()
    keys_pressed = [0, 0, 0, 0]  # The pressed status of the keys
    start = True
    score = 0

    """if draw:
        while start:
            events = get_events()

            keys = pygame.key.get_pressed()
            keys_down = [idx for idx, val in enumerate(keys) if val == 1]
            event_keys = (pygame.K_SPACE, 0)
            key_states = [int(key in keys_down) for key in event_keys]
            if key_states[0] is 1:
                start = False

            view.draw_start(size)
"""
    reset_car(world, map_name)
    # print(world.car.position)

    while True:
        # This block of code generates a list of each key's pressed status (0=up, 1=pressed)
        # The list is for keys [W, S, A, D]
        events = get_events()

        if draw:
            # draws the map, car and button
            view.draw_scene(world, events)
            view.press_button(events)
        if control:
            keys_pressed = get_input()

            world.car.driving_force = (keys_pressed[0] * FORCE - keys_pressed[1] * BRAKING)
            world.car.steering = (keys_pressed[2]-keys_pressed[3]) * INCREMENT
        else:
            # Of the form (turn, accelerator)
            d_steer, d_gas = world.car.sensors.calculate_changes(autopilot)

            if d_gas > 1:
                d_gas = 1
            if d_gas < -1:
                d_gas = -1

            # print(d_gas)
            world.car.driving_force = 2.5 * d_gas * FORCE
            world.car.steering = atan(d_steer / d_gas)

        if world.car.steering > steering_max:
            world.car.steering = steering_max
        elif world.car.steering < -steering_max:
            world.car.steering = -steering_max

        world.car.update_pos(world.road)

        hold, position_score = world.car.update_score(world.reward_matrix)
        if hold == -1:
            # print('WENT DOWN IN VALUE:', score)
            reset_car(world)
            if world.car.time_score < 150:
                return 0
            elif position_score <= .01 and world.car.speed_total > 10000:
                score += world.car.average_speed
            return score
        else:
            score = hold

        if world.car.time_score > 60 and position_score < 1:
            if np.all(world.reward_matrix == 0):
                pass
            else:
                return 0
        if world.detect_crash():  # If the car has crashed, reset it
            reset_car(world, map_name)

            # print('FINAL SCORE:', score)
            if position_score == world.reward_matrix.max() and world.car.time_score < 50:
                score = 0
            return score


def reset_car(world, map_name="NONE"):
    # print('Attempting to Reset Car')
    try:
        if map_name is not 'NONE':
            file_add = map_name + '/'
        else:
            file_add = ''
        temp_position, temp_angle = pickle.load(open(file_add + "pos_ang.p", "rb"))
        # print(temp_position)

        world.car_start_pos = temp_position
        world.car_start_angle = temp_angle
        world.reset_car()
    except:
        # print('Reset Failed. Draw New Track')
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
    keys = pygame.key.get_pressed()
    keys_down = [idx for idx, val in enumerate(keys) if val == 1]
    # The event values representing the keys pressed
    event_keys = (pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a)
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
    main()
