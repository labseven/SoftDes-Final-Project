from sensors import sensors
from physics import physics


class Car():
    """
    The car. Has sensors, position, can accelerate, and turn the wheels.
    """

    def __init__(self, world_map, init_pos, init_angle, init_vel, mass=500, moment=200, car_color=(124, 124, 124)):
        self.position = init_pos
        self.angle = init_angle
        self.velocity = init_vel
        self.mass = mass
        self.moment = moment
        self.steering = 0
        self.accelerometer = 0
        self.size = (mass/50, mass/25)
        self.color = car_color
        self.sensors = Sensors(self, world_map)


    def update_pos(self):
        # F_net and T_net are inputs from keyboard or autonomous
        F_net = [10,0]
        delta_time = .1
        [self.position, self.velocity, self.angle] = physics(self.position, self.velocity, self.angle, delta_time, self.mass, self.moment)
