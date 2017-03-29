import car
import sensors
import physics
import world
from view import *



def main():
    view = View()

    clock = pygame.time.Clock()

    while True:
        view.draw_scene()
        clock.tick(60)


if __name__ == "__main__":
    main()
