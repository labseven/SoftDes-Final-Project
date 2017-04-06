from world import World
from view import View
import pygame
from math import sin, cos


def main():
    size = (1000, 1000)
    world = World(size)

    view = View(size=size, map_in=world)

    clock = pygame.time.Clock()
    keys_pressed = [0, 0, 0, 0]  # The pressed status of the keys

    while True:
        # This block of code generates a list of each key's pressed status (0=up, 1=pressed)
        # The list is for keys [W, S, A, D]
        keys_pressed = get_input()

        # Changes angular velocity based on keys pressed (should be changed to make it accelerate)
        world.car.velocity[0] = -(-keys_pressed[0]+keys_pressed[1])*-sin(world.car.angle[0])*100
        world.car.velocity[1] = -(-keys_pressed[0]+keys_pressed[1])*cos(world.car.angle[0])*100
        world.car.angle[1] = (keys_pressed[2]-keys_pressed[3])
        view.draw_scene(world)
        world.car.update_pos()

        clock.tick(60)


def get_input():
    """
    Returns a list of user input values (keys, mouse presses, mouse pos).
    """
    keys = pygame.key.get_pressed()
    keys_down = [idx for idx, val in enumerate(keys) if val == 1]
    event_keys = (pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a)
    key_states = [int(key in keys_down) for key in event_keys]
    return key_states


if __name__ == "__main__":
    main()
