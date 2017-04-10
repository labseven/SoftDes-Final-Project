from world import World
from view import View
import pygame
from math import pi
FORCE = -500
BRAKING = -1000
INCREMENT = pi / 100
steering_max = pi/2-.1

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

        world.car.driving_force = (keys_pressed[0] * FORCE - keys_pressed[1] * BRAKING)
        world.car.steering += (keys_pressed[2]-keys_pressed[3]) * INCREMENT
        if world.car.steering > steering_max:
            world.car.steering = steering_max
        elif world.car.steering < -steering_max:
            world.car.steering = -steering_max

        view.draw_scene(world)
        world.car.update_pos()
        clock.tick(60)


if __name__ == "__main__":
    main()
