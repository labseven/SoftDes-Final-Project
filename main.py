import car
import sensors
import physics
import world


class Scene():
    def __init__(self, window_size=(1000,1000)):
        """
        Initializes the scene
        """
        self.window_size = window_size
        self.world = World(window_size)
        pygame.init()
        self.canvas = pygame.display.set_mode(self.window_size, 0, 32)


def main():
    scene = Scene()

    clock = pygame.time.Clock()

    while True:
        scene.render_scene()
        clock.tick(60)

if __name__ == '__main__':
    main()
