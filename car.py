
import car_physics
from sensors import Sensors
import numpy as np
import math

class Car():
    """
    The car. Has sensors, position, can accelerate, and turn the wheels.
    """

    def __init__(self, road, world_size, init_pos, init_angle, init_vel, mass=500, moment=200, car_color=(124, 124, 124)):
        car_width = 16
        car_height = 32
        self.L_R = np.matrix([[-car_width / 2], [car_height / 2]])
        self.L_F = np.matrix([[-car_width / 2], [-car_height / 2]])
        self.R_R = np.matrix([[car_width / 2], [car_height / 2]])
        self.R_F = np.matrix([[car_width / 2], [-car_height / 2]])

        self.speed_total = 0
        self.iterations = 0

        self.init_angle = init_angle

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
        self.current_position_score = 0
        self.score = 0

    def update_pos(self, road):
        # F_net and T_net are inputs from keyboard or autonomous
        self.time_score += .1
        self.sensors.update_road(road)
        delta_time = .1
        self.update_hitpoints()
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
        self.iterations += 1
        self.speed_total += (self.velocity[0]**2 + self.velocity[1]**2)**.5
        self.average_speed = self.speed_total / self.iterations

        self.lidar_distances, self.lidar_hits = self.sensors.get_lidar_data()

    def update_hitpoints(self):
        theta = -self.angle[0]
        rotation_matrix = np.matrix([[math.cos(theta), -1 * math.sin(theta)],
                                     [math.sin(theta), math.cos(theta)]])
        position_matrix = np.matrix([[self.position[0]], [self.position[1]]])

        potential_fix = np.matrix([[math.cos(self.init_angle[0])*self.sprite_w-8], [math.sin(-self.init_angle[0])*self.sprite_w+16]])

        back_l = rotation_matrix * self.L_R + position_matrix + potential_fix
        frnt_l = rotation_matrix * self.L_F + position_matrix + potential_fix
        back_r = rotation_matrix * self.R_R + position_matrix + potential_fix
        frnt_r = rotation_matrix * self.R_F + position_matrix + potential_fix

        back_l = ((int)(back_l.item(0)), (int)(back_l.item(1)))
        frnt_l = ((int)(frnt_l.item(0)), (int)(frnt_l.item(1)))
        back_r = ((int)(back_r.item(0)), (int)(back_r.item(1)))
        frnt_r = ((int)(frnt_r.item(0)), (int)(frnt_r.item(1)))
        # print((back_l[0]**2 + back_l[1]**2)**.5)
        # print([(int)(back_l[0]-x_pos), (int)(back_l[1]-y_pos)], [(int)(frnt_l[0]-x_pos), (int)(frnt_l[1]-y_pos)], [(int)(back_r[0]-x_pos), (int)(back_r[1]-y_pos)], [(int)(frnt_r[0]-x_pos), (int)(frnt_r[1]-y_pos)])
        # print([(int)(back_l[0]), (int)(back_l[1])], [(int)(frnt_l[0]), (int)(frnt_l[1])], [(int)(back_r[0]), (int)(back_r[1])], [(int)(frnt_r[0]), (int)(frnt_r[1])])

        # car.points = [new_rect.topleft, new_rect.topright, new_rect.bottomright, new_rect.bottomleft]
        # print(back_l)
        self.points = [back_l, frnt_l, frnt_r, back_r]

    def update_score(self, value_map):
        try:
            map_x = int(self.position[0])
            map_y = int(self.position[1])
            self.current_position_score = value_map[map_y][map_x]
        except(IndexError):
            self.current_position_score = 0
        if self.current_position_score < self.last_position_score:
            return(-1, self.current_position_score)
        self.last_position_score = self.current_position_score
        # print(current_position_score, end='\r')
        self.score = self.current_position_score # self.speed_total/1000
        # print(self.average_speed)
        return(self.score, self.current_position_score)
