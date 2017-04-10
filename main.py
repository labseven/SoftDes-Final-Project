from world import World
from view import View
import pygame
from math import pi
FORCE = -500
BRAKING = -1000
INCREMENT = pi / 100
steering_max = pi/2-.1

import sys


def main():
    size = (1000, 1000)
    world = World(size)

    view = View(size=size, map_in=world)

    clock = pygame.time.Clock()
    keys_pressed = [0, 0, 0, 0]  # The pressed status of the keys

    while True:
        # This block of code generates a list of each key's pressed status (0=up, 1=pressed)
        # The list is for keys [W, S, A, D]
        events = get_events()
        keys_pressed = get_input()
        mouse_down = get_mouse_drawing(events)

        world.car.driving_force = (keys_pressed[0] * FORCE - keys_pressed[1] * BRAKING)
        world.car.steering += (keys_pressed[2]-keys_pressed[3]) * INCREMENT
        if world.car.steering > steering_max:
            world.car.steering = steering_max
        elif world.car.steering < -steering_max:
            world.car.steering = -steering_max


        view.draw_scene(world, events)
        world.car.update_pos()

        view.press_button(events)

        clock.tick(60)


def get_events():
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    return events


def get_input():
    """
    Returns a list of user input values (keys, mouse presses, mouse pos).
    """
    keys = pygame.key.get_pressed()
    keys_down = [idx for idx, val in enumerate(keys) if val == 1]
    event_keys = (pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a)
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
