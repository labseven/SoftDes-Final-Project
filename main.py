from world import World
from view import *


def main():
    view = View()
    world = World((1000, 1000))

    clock = pygame.time.Clock()

    while True:
        view.draw_scene(world)
        clock.tick(60)


if __name__ == "__main__":
    main()
