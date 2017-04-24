"""
Class that holds the state variables of the car.

@author Alex Chapman
(c) April 2017

"""
import car_physics
from sensors import Sensors
import numpy as np
import math


class Car():
    """
    The car. Has sensors, position, can accelerate, and turn the wheels.
    """

    def __init__(self, road, world_size, init_pos, init_angle, init_vel, mass=500, moment=200, car_color=(124, 124, 124)):
        """
            Creates a car with the initial state values.
            Inputs:
                road        matrix holding the values of the road (255 for road, 0 for bg)
                world_size  double tuple holding width / height of window and road
                init_pos    tuple holding (x, y)
                init_angle  tuple holding (angle, angular velocity)
                init_vel    tuple holding (v_x, v_y)
                mass        mass of car in kg
                moment      moment of inertia of car in kg m^2
                car_color   RGB color values of car drawn as a rectangle. Redundant but possibly useful

            Source for moment:
            https://www.degruyter.com/downloadpdf/j/mecdc.2013.11.issue-1/mecdc-2013-0003/mecdc-2013-0003.pdf
        """
        # size of sprite in pixels
        car_width = 16
        car_height = 32

        # Vectors describing the corners of the hitbox
        self.L_R = np.matrix([[-car_width / 2], [car_height / 2]])
        self.L_F = np.matrix([[-car_width / 2], [-car_height / 2]])
        self.R_R = np.matrix([[car_width / 2], [car_height / 2]])
        self.R_F = np.matrix([[car_width / 2], [-car_height / 2]])

        # Initial state things
        self.init_angle = init_angle
        self.position = init_pos
        self.angle = init_angle
        self.velocity = init_vel
        self.steering = 0

        # Physics things
        self.mass = mass
        self.moment = moment
        self.size = (4, 8)
        self.sensors = Sensors(self, road, world_size)

        # Drawing things
        self.color = car_color
        self.lidar_distances = []
        self.lidar_hits = []
        self.sprite_w = 16
        self.sprite_h = 32
        self.visible = False
        self.points = [(0, 0), (0, 0), (0, 0), (0, 0)]

        # Scoring things, primarily for evolution
        self.speed_total = 0
        self.iterations = 0
        self.time_score = 0
        self.current_position_score = 0
        self.last_position_score = 0
        self.score = 0

    def update_pos(self, road):
        """
        Calls the physics functions and updates the state of the car.
        Moves car one time step.
        Applies physics based on state variables, including velocity,
        accelerometer input, and steering wheel input.

        Updates car position and sensor readouts.
        """
        delta_time = .1

        self.sensors.update_road(road)  # Updates lidar
        self.lidar_distances, self.lidar_hits = self.sensors.get_lidar_data()
        self.update_hitpoints()  # updates hitbox so that it follows car

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
        self.time_score += delta_time

    def update_hitpoints(self):
        """
        Uses the rotation matrix to rotate the hitbox of the car. Then adds
        position to get a box that fits the car exactly.
        """
        theta = -self.angle[0]  # To correct for inversion between pygame and physics

        # Source: https://en.wikipedia.org/wiki/Rotation_matrix
        rotation_matrix = np.matrix([[math.cos(theta), -1 * math.sin(theta)],
                                     [math.sin(theta), math.cos(theta)]])

        position_matrix = np.matrix([[self.position[0]], [self.position[1]]])

        # Fixes issue of hitbox being translated up and left
        translation = np.matrix([[math.cos(self.init_angle[0])*self.sprite_w-8], [math.sin(-self.init_angle[0])*self.sprite_w+16]])

        # Saves all 4 points as numpy matrices
        back_l = rotation_matrix * self.L_R + position_matrix + translation
        frnt_l = rotation_matrix * self.L_F + position_matrix + translation
        back_r = rotation_matrix * self.R_R + position_matrix + translation
        frnt_r = rotation_matrix * self.R_F + position_matrix + translation

        # breaks up all points into tuples
        back_l = ((int)(back_l.item(0)), (int)(back_l.item(1)))
        frnt_l = ((int)(frnt_l.item(0)), (int)(frnt_l.item(1)))
        back_r = ((int)(back_r.item(0)), (int)(back_r.item(1)))
        frnt_r = ((int)(frnt_r.item(0)), (int)(frnt_r.item(1)))

        self.points = [back_l, frnt_l, frnt_r, back_r]

    def update_score(self, value_map):
        """
        Updates the fitness of the car based on how far around the track it has gotten.
        """
        try:
            map_x = int(self.position[0])
            map_y = int(self.position[1])
            self.current_position_score = value_map[map_y][map_x]
        except(IndexError):  # tries to read position, if invalid it sets score to 0
            self.current_position_score = 0

        # Establishes going down in value is bad
        if self.current_position_score < self.last_position_score:
            return(-1, self.current_position_score)

        # Saves score as last score, returns
        self.last_position_score = self.current_position_score
        self.score = self.current_position_score
        return(self.score, self.current_position_score)
