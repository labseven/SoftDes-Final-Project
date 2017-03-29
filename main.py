from world import World
from view import View
import pygame
from math import sin, cos


def main():
    view = View()
    world = World((1000, 1000))

    clock = pygame.time.Clock()
    event_keys = (pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a)
    keys_pressed = [0, 0, 0, 0]  # The pressed status of the keys

    while True:
        # This block of code generates a list of each key's pressed status (0=up, 1=pressed)
        # The list is for keys [W, S, A, D]
        events = pygame.event.get()  # Gets all events
        down_keys = [event.key for event in events if event.type == pygame.KEYDOWN]
        up_keys = [event.key for event in events if event.type == pygame.KEYUP]
        for idx in range(4):
            keys_pressed[idx] += int(event_keys[idx] in down_keys) - int(event_keys[idx] in up_keys)

        # Changes angular velocity based on keys pressed (should be changed to make it accelerate)
        world.car.velocity[0] = (-keys_pressed[0]+keys_pressed[1])*-sin(world.car.angle[0])*100
        world.car.velocity[1] = (-keys_pressed[0]+keys_pressed[1])*cos(world.car.angle[0])*100
        world.car.angle[1] = keys_pressed[2]-keys_pressed[3]

        view.draw_scene(world)
        world.car.update_pos()
        clock.tick(60)


if __name__ == "__main__":
    main()
