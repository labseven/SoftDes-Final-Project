import car
import sensors
import physics
from world import *
from view import *


def main():
    size = (1000,1000)
    view = View()
    world = World(size)

    clock = pygame.time.Clock()

    while True:
        view.draw_scene()
        view.car.update_pos()
        print("Distance:", view.car.sensors.get_lidar_distance(0))
        clock.tick(60)


if __name__ == "__main__":
    main()
