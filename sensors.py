"""
Current Sensors:

Lidar with n points
Accelerometer
Spedometer
"""

from math import sin, cos, sqrt

class Sensors:
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


    def get_lidar_data(self):
        """
        Outputs a list of distances.
        """
        distances = []
        for angle in self.lidar_angels:
            distances.append(get_lidar_distance(angle))

        return distances


    def get_lidar_distance(angle):
        """
        Returns the distancs from lidar position to nearest wall, in the
        direction of angle.
        """

        locationX = self.car.position[0]
        locationY = self.car.position[1]
        # Position in map
        mapX = int(locationX)
        mapY = int(locationY)

        ray_angle = angle + self.car.angle
        dirX = sin(ray_angle)
        dirY = cos(ray_angle)

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

        print("Step:", stepX,stepY, "sideDist", sideDistX,sideDistY)


        # Step through boxes until you hit a wall
        while(True):
            if sideDistX < sideDistY:
                sideDistX += deltaDistX
                mapX += stepX
                side = 0
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1
            if self.car.world.world_map[mapX][mapY] == 1:
                break

        print("Hit at:", mapX, mapY)
        return 1


if __name__ == '__main__':
    pass
