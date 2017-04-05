"""
@Author: Adam Novotny

The sensor class
"""

from math import sin, cos, sqrt, pi
import numpy as np


class Sensors():
    """
    Sensor implemented:
    Lidar with n points
    """
    def __init__(self, car, road, world_size, lidar_num = 20, lidar_max_angle = pi-.01):
        """
        Initializes the sensor class.
        """

        self.car = car
        self.road = road
        self.world_size = world_size

        self.lidar_angles = []
        # Add equally spaced sensors
        lidar_spacing = (2 * lidar_max_angle) / (lidar_num)

        for i in range(lidar_num):
            self.lidar_angles.append(-lidar_max_angle + (i * lidar_spacing))

    def get_lidar_data(self):
        """
        Outputs a list of distances.
        """
        distances = []
        hit_pos = []
        for angle in self.lidar_angles:
            lidar = self.get_lidar_distance(angle)
            distances.append(lidar[0])
            hit_pos.append(lidar[1])

        return distances, hit_pos


    def get_lidar_distance(self, angle):
        """
        Returns the distancs from lidar position to nearest wall, in the
        direction of angle.
        """

        locationX = self.car.position[0]
        locationY = self.car.position[1]
        # Position in map
        mapX = int(locationX)
        mapY = int(locationY)

        # What the value of the map where the car is at
        try:
            curr_map_value = self.road[mapX][mapY]
        except:
            curr_map_value = 0
        # print(self.car.angle[0])
        ray_angle = angle - self.car.angle[0]

        dirX = sin(ray_angle)
        dirY = cos(ray_angle)

        if dirX == 0:
            deltaDistX = 0 # Might be wrong
        else:
            deltaDistX = sqrt(1 + dirY**2 / dirX**2)

        if dirY == 0:
            deltaDistY = 0 # Might be wrong
        else:
            deltaDistY = sqrt(1 + dirX**2 / dirY**2)

        if (dirX < 0):
            stepX = -1
            sideDistX = (locationX - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX - locationX + 1) * deltaDistX

        if (dirY < 0):
            stepY = -1
            sideDistY = (locationY - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY - locationY + 1) * deltaDistY

        # print("Step:", stepX,stepY, "sideDist", sideDistX, sideDistY)


        # Step through boxes until you hit a wall
        while(True):
            # Step in the shorter side dist
            if sideDistX < sideDistY:
                sideDistX += deltaDistX
                mapX += stepX
                side = 0
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1
            # Hit edge of map
            if mapX <= 0 or mapX >= self.world_size[0]-1 or mapY <= 0 or mapY >= self.world_size[1]-1:
                break
            # if self.car.world.world_map[mapX][mapY] == 1:
            if self.road[mapX][mapY] != curr_map_value:
                break

        # print("Hit at:", mapX, mapY)
        # print("sideDist:", sideDistX, sideDistY)

        distance = sqrt((mapX-locationX)**2 + (mapY-locationY)**2)

        return distance, [mapX, mapY]


if __name__ == '__main__':
    pass
