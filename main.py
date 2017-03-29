from car import Car
from view import View
import sensors
import physics
from world import World
import pygame


class Scene():
    def __init__(self, window_size=(1000,1000)):
        """
        Initializes the scene
        """
        self.window_size = window_size
        self.world = World(window_size)
        pygame.init()
        self.view = View(world=self.world)


def main():
    scene = Scene()

    clock = pygame.time.Clock()

    while True:
        scene.view.draw_scene(scene.world)

        clock.tick(60)

if __name__ == '__main__':
    main()
