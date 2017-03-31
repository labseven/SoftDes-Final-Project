import physics
import car_physics


class Car:
    """
    The car. Has sensors, position, can accelerate, and turn the wheels.
    """

    def __init__(self, init_pos, init_angle, init_vel,
                 mass=500, moment=200, car_color=(124, 124, 124)):
        self.position = init_pos
        self.angle = init_angle
        self.velocity = init_vel
        self.mass = mass
        self.moment = moment
        self.steering = 0
        self.accelerometer = 0
        self.size = (mass/50, mass/25)
        self.color = car_color

    def update_pos(self):
        # F_net and T_net are inputs from keyboard or autonomous
        delta_time = .1
        # [self.position, self.velocity, self.angle] = physics.physics(self.position, self.velocity, self.angle, delta_time, self.mass, self.moment)
        [self.position,
         self.velocity,
         self.angle] = car_physics.update_physics(self.position,
                                                  self.velocity,
                                                  self.angle,
                                                  self.steering,
                                                  self.driving_force,
                                                  self.mass,
                                                  self.moment,
                                                  delta_time)
        # # Update lidar position
        # self.lidar_pos[0] = self.car.position[0] + cos(angle) * self.car.lidar_pos[0] + sin(angle) * self.car.lidar_pos[1]
        # self.lidar_pos[1] = self.car.position[1] + sin(angle) * self.car.lidar_pos[0] + cos(angle) * self.car.lidar_pos[1]
