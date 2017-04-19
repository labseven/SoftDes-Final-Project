
import car_physics
from sensors import Sensors


class Car():
    """
    The car. Has sensors, position, can accelerate, and turn the wheels.
    """

    def __init__(self, road, world_size, init_pos, init_angle, init_vel, mass=500, moment=200, car_color=(124, 124, 124)):
        self.position = init_pos
        self.angle = init_angle
        self.velocity = init_vel
        self.mass = mass
        self.moment = moment
        self.steering = 0
        self.accelerometer = 0

        # Sensors
        self.sensors = Sensors(self, road, world_size)
        self.lidar_distances = []
        self.lidar_hits = []

        # Drawing things
        self.color = car_color
        self.sprite_w = 16
        self.sprite_h = 32
        self.visible = False
        self.points = [(0, 0), (0, 0), (0, 0), (0, 0)]

    def update_pos(self, road):
        """
        Moves car one time step.
        Applies physics based on state variables, including velocity,
        accelerometer input, and steering wheel input.

        Updates car position and sensor readouts.
        """
        self.sensors.update_road(road)
        delta_time = .09

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

        self.lidar_distances, self.lidar_hits = self.sensors.get_lidar_data()
