from world import World
from view import View
import pygame
from math import pi
FORCE = -1000
BRAKING = -500
steering_max = pi/2-.1
INCREMENT = pi/4


def main(draw=True, autopilot=[0, 0, 0, 0, 0, 0, 0, 0]):
    size = (1000, 1000)
    world = World(size)

    view = View(size=size, map_in=world)

    clock = pygame.time.Clock()
    keys_pressed = [0, 0, 0, 0]  # The pressed status of the keys
    start = True

    if draw:
        while start:
            events = get_events()

            keys = pygame.key.get_pressed()
            keys_down = [idx for idx, val in enumerate(keys) if val == 1]
            event_keys = (pygame.K_SPACE, 0)
            key_states = [int(key in keys_down) for key in event_keys]
            if key_states[0] is 1:
                start = False

            view.draw_start(size)

    while True:
        # This block of code generates a list of each key's pressed status (0=up, 1=pressed)
        # The list is for keys [W, S, A, D]
        if draw:
            events = get_events()
            keys_pressed = get_input()

            world.car.driving_force = (keys_pressed[0] * FORCE - keys_pressed[1] * BRAKING)
            world.car.steering = (keys_pressed[2]-keys_pressed[3]) * INCREMENT

            # draws the map, car and button
            view.draw_scene(world, events)
            view.press_button(events)

        # Of the form (turn, accelerator)
        # pilot_commands = sensors.calculate_changes(autopilot)

        if world.car.steering > steering_max:
            world.car.steering = steering_max
        elif world.car.steering < -steering_max:
            world.car.steering = -steering_max

        world.car.update_pos(world.road)

        score = world.car.update_score(world.reward_matrix)

        print(score, end='\r')
        if world.detect_crash():  # If the car has crashed, reset it
            print('FINAL SCORE:', score)
            return score

        clock.tick(60)


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
