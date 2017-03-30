from physics import *
from sensors import *


class Car():
    """
    The car. Has sensors, position, can accelerate, and turn the wheels.
    """

    def __init__(self, init_pos, init_angle, mass = 500, moment = 200):
        self.position = init_pos
        self.angle = init_angle
        self.velocity = [0,0]
        self.mass = mass
        self.moment = moment
        self.steering = 0
        self.accelerometer = 0
        self.size = (100, 100)
        self.color = (124, 124, 124)
        self.sensors = Sensors(self)


    def update_pos(self):
        # F_net and T_net are inputs from keyboard or autonomous
        F_net = [10,0]
        delta_time = .1
        [self.position, self.velocity, self.angle] = physics(self.position, self.velocity, self.angle, delta_time, self.mass, self.moment)
        print("Car pos:", self.position)
        # # Update lidar position
        # self.lidar_pos[0] = self.car.position[0] + cos(angle) * self.car.lidar_pos[0] + sin(angle) * self.car.lidar_pos[1]
        # self.lidar_pos[1] = self.car.position[1] + sin(angle) * self.car.lidar_pos[0] + cos(angle) * self.car.lidar_pos[1]
