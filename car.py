class Car:
    """
    The car. Has sensors, position, can accelerate, and turn the wheels.
    """

    def __init__(self, world, init_pos, init_angle):
        self.position = init_pos
        self.angle = init_angle

    def update_pos(self):
        """
        Updates its position.
        """

        self.lidar_pos[0] = self.car.position[0] + cos(angle) * self.car.lidar_pos[0] + sin(angle) * self.car.lidar_pos[1]
        self.lidar_pos[1] = self.car.position[1] + sin(angle) * self.car.lidar_pos[0] + cos(angle) * self.car.lidar_pos[1]
