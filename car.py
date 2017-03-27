import physics


class Car:
    """
    The car. Has sensors, position, can accelerate, and turn the wheels.
    """

    def __init__(self, world, init_pos, init_angle, lidar_pos, mass = 500, moment = 200):
        self.position = init_pos
        self.angle = init_angle
        self.lidar_car_pos = lidar_pos
        self.velocity = [0,0]
        self.mass = mass
        self.moment = moment


    def update_pos(self):
        [self.position, self.velocity, self.angle] = physics.physics(self.position, self.velocity, self.angle, F_net=0, T_net=0, dt=delta_time, self.mass, self.moment)

        self.lidar_pos[0] = self.car.position[0] + cos(angle) * self.car.lidar_pos[0] + sin(angle) * self.car.lidar_pos[1]
        self.lidar_pos[1] = self.car.position[1] + sin(angle) * self.car.lidar_pos[0] + cos(angle) * self.car.lidar_pos[1]
