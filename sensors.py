"""
Current Sensors:

Lidar with n points
Accelerometer
Spedometer
"""

from math import sin, cos, sqrt
import numpy as np

class Sensors():
    """
    All sensor things.

    Has a world and car attached to it.
    """
    def __init__(self, car, lidar_num = 9, lidar_max_angle = 90):
        """
        Initializes the sensor class.
        """

        self.car = car
        self.lidar_angels = []

        # Add equally spaced sensors
        lidar_spacing = lidar_num / (2 * lidar_max_angle)
        for i in range(lidar_num):
            self.lidar_angels.append(-lidar_max_angle + (i * lidar_spacing))


        # Hardcoded world map until we refactor
        size = (1000,1000)
        self.world_map = np.zeros(size)
        self.world_map_size = size
        # Quick wall for testing
        for i in range(size[0]):
            self.world_map[i][i] = 1
        print("Made sensor world_map")


    def get_lidar_data(self):
        """
        Outputs a list of distances.
        """
        distances = []
        for angle in self.lidar_angels:
            distances.append(get_lidar_distance(angle))

        return distances


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

        print(self.car.angle[0])
        ray_angle = angle + self.car.angle[0]
        dirX = sin(ray_angle)
        dirY = cos(ray_angle)

        if dirX == 0:
            deltaDistX = 0
        else:
            deltaDistX = sqrt(1 + dirY**2 / dirX**2)
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

        print("Step:", stepX,stepY, "sideDist", sideDistX, sideDistY)


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
            if mapX >= self.world_map_size[0]-1 or mapY >= self.world_map_size[1]-1:
                break
            # if self.car.world.world_map[mapX][mapY] == 1:
            if self.world_map[mapX][mapY] == 1:
                break

        print("Hit at:", mapX, mapY)
        print("sideDist:", sideDistX, sideDistY)

        distance = sqrt((mapX-locationX)**2 + (mapY-locationY)**2)

        return distance


if __name__ == '__main__':
    pass
