
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
        self.size = (4, 8)
        self.last_position_score = 0
        self.sensors = Sensors(self, road, world_size)

        # Drawing things
        self.color = car_color
        self.sensors = Sensors(self, road, world_size)
        self.lidar_distances = []
        self.lidar_hits = []
        self.sprite_w = 16
        self.sprite_h = 32
        self.visible = False
        self.points = [(0, 0), (0, 0), (0, 0), (0, 0)]

        self.time_score = 0
        self.points = 0

    def update_pos(self, road):
        # F_net and T_net are inputs from keyboard or autonomous
        self.time_score += .1
        self.sensors.update_road(road)
        delta_time = .1

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

    def update_score(self, value_map):
        map_x = int(self.position[0])
        map_y = int(self.position[1])
        current_position_score = value_map[map_y][map_x]
        if current_position_score < self.last_position_score:
            return -1
        self.last_position_score = current_position_score
        # print(current_position_score, end='\r')
        self.score = current_position_score  # + self.time_score
        return self.score
