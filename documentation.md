# Map coordinate system:
Origin:

# Class variables:

## Car:
- position - current world position
- orientation - current world orientation
- lidar_car_pos - position of lidar relative to origin of car (when pointing north)
- lidar_world_pos - position of the lidar in the world
- world - the world the car is in


## Sensors:
- car - the car the sensors are on
- lidar_angels - the angles of the lidar

## World:
- world_map - 2D array holding the map
- materials = [[R, G, B], "name"] - list of materials of the map - will be expanded to hold traction or other relevant data
