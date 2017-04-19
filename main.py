from world import World
from view import View
import pygame
from math import pi
FORCE = -500
BRAKING = -1000
INCREMENT = pi / 10
steering_max = pi/2-.1


def main():
    size = (1000, 1000)
    world = World(size)

    view = View(size=size, map_in=world)

    clock = pygame.time.Clock()
    keys_pressed = [0, 0, 0, 0]  # The pressed status of the keys
    start = True

    pygame.mixer.music.load('assets/corn_racer.mp3')
    pygame.mixer.music.play(loops=-1)
    while start:
        events = get_events()

        keys = pygame.key.get_pressed()
        keys_down = [idx for idx, val in enumerate(keys) if val == 1]
        event_keys = (pygame.K_SPACE, 0)
        key_states = [int(key in keys_down) for key in event_keys]
        if key_states[0] is 1:
            start = False

        view.draw_start(size)

    pygame.mixer.music.stop()
    low_sound = pygame.mixer.Sound('assets/car_low.ogg')
    low_sound.set_volume(0)
    low_sound.play(loops=-1, fade_ms=100)

    high_sound = pygame.mixer.Sound('assets/car_high.ogg')
    high_sound.set_volume(0)
    high_sound.play(loops=-1, fade_ms=100)

    crash_sound = pygame.mixer.Sound('assets/crash.ogg')

    while True:
        # This block of code generates a list of each key's pressed status (0=up, 1=pressed)
        # The list is for keys [W, S, A, D]
        events = get_events()
        keys_pressed = get_input()

        world.car.driving_force = (keys_pressed[0] * FORCE - keys_pressed[1] * BRAKING)
        world.car.steering = (keys_pressed[2]-keys_pressed[3]) * INCREMENT
        if world.car.steering > steering_max:
            world.car.steering = steering_max
        elif world.car.steering < -steering_max:
            world.car.steering = -steering_max

        # draws the map, car and button
        view.draw_scene(world, events)
        world.car.update_pos(world.road)

        view.press_button(events)
        world.detect_collisions()

        if world.car.visible:
            velocity = world.car.velocity[0]**2 + world.car.velocity[1]**2 # 100 is slow, 200 is medium, 300 is fast
            volume = (velocity - 150) / 250
            if volume > 1:
                volume = 1
            if volume < 0:
                volume = 0

            print("\n", volume, "\r\r")
            low_sound.set_volume(.5)
            high_sound.set_volume(volume)

        if world.car.visible:
            if world.detect_crash():  # If the car has crashed, reset it
                crash_sound.play()
                world.reset_car()

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
