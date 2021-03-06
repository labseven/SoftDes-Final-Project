"""
@Author: Adam Novotny

The Sensor class
"""

from math import sin, cos, sqrt, pi

class Sensors():
    """ Sensor class. Returns sensor values.

    Sensors implemented:
    Lidar with n points
    """
    def __init__(self, car, road, world_size, lidar_num=20, lidar_max_angle=pi-.01):
        self.car = car
        self.road = road
        self.world_size = world_size

        # Create equally spaced sensors
        self.lidar_angles = []
        lidar_spacing = (2 * -lidar_max_angle) / (lidar_num)

        for i in range(lidar_num):
            self.lidar_angles.append(lidar_max_angle + (i * lidar_spacing))
            # print((lidar_max_angle + (i * lidar_spacing))*180 / pi)

    def calculate_changes(self, autopilot):
        distances = self.get_lidar_data()
        angles = self.lidar_angles
        x_vals = 0.0
        y_vals = 0.0
        for distance in distances:
            for idx, dist in enumerate(distance):
                if idx == 0:
                    idx = 1
                else:
                    if type(dist) is float:
                        x_vals += ((float)(autopilot[idx]) * dist * cos(angles[idx]))
                        y_vals += ((float)(autopilot[idx]) * dist * sin(angles[idx]))

        return((x_vals, y_vals))

    def update_road(self, road):
        self.road = road

    def get_lidar_data(self, lidar_angles=None):
        """ Outputs a list of lidar distances.
        """
        if lidar_angles is None:
            lidar_angles = self.lidar_angles

        distances = []
        hit_pos = []
        for angle in lidar_angles:
            lidar = self.get_lidar_distance(angle)
            distances.append(lidar[0])
            hit_pos.append(lidar[1])

        return distances, hit_pos

    def get_lidar_distance(self, angle, return_square_dist=False):
        """ Return the distance from car to the nearest wall, in the direction
        of angle. Also returns coordinates of lidar hit.


        Uses raycasting to find the hit location.
        See (lodev.org/cgtutor/raycasting.html) for more information.

        Input: angle of ray (relative to car), return_square_distance (for performance)
        Returns: Distance, [mapX, mapY]
        """

        locationX = self.car.position[0]
        locationY = self.car.position[1]

        # Position in map
        mapX = int(locationX)
        mapY = int(locationY)

        # Save the value of the map where the car currently is
        # Ray goes until the map changes values
        try:
            curr_map_value = self.road[mapX][mapY]
            # print(curr_map_value)
        except:
            # If off the screen
            # print("Off the screen")
            curr_map_value = 0

        if curr_map_value == 0:
            # print("Crashed", end='\r')
            # raise StopIteration
            pass
        ray_angle = angle + self.car.angle[0]

        dirX = sin(ray_angle)
        dirY = cos(ray_angle)

        # Set deltaDist based on angle. Ifs are to remove divide by zero.
        # sideDist is incremented by deltaDist every x or y step
        if dirX == 0:
            deltaDistX = 0
        else:
            deltaDistX = sqrt(1 + dirY**2 / dirX**2)

        if dirY == 0:
            deltaDistY = 0
        else:
            deltaDistY = sqrt(1 + dirX**2 / dirY**2)

        # Set init sideDist and what direction to step
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

        # Step through boxes until you hit a wall
        while(True):
            # Step in the direction of the shorter sideDist
            # This makes the steps follow the actual slope of the ray
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
            # Hit something that is not the current map value
            if self.road[mapX][mapY] != curr_map_value:
                break

        # Whether to return square of the distance (for performance)
        if return_square_dist:
            distance = (mapX-locationX)**2 + (mapY-locationY)**2
        else:
            distance = sqrt((mapX-locationX)**2 + (mapY-locationY)**2)

        return distance, [mapX, mapY]
