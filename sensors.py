"""
Current Sensors:

Lidar with n points
Accelerometer
Spedometer
"""

from math import sin, cos

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
        # Position in map
        mapX = int(self.car.lidar_world_pos[0])
        mapY = int(self.car.lidar_world_pos[1])

        ray_angle = angle + self.car.angle


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

        return 1
