# Coordinate systems:
Map Origin: Top left
Map direction: right, down

Car Origin: Center


# Class variables:

## Car:
- position - current world position
- orientation - current world orientation
- world - the world the car is in


## Sensors:
- car - the car the sensors are on
- lidar_angels - the angles of the lidar

## World:
- world_map - 2D array holding the map
- materials = [[R, G, B], "name"] - list of materials of the map - will be expanded to hold traction or other relevant data

## Map
0 - Empty
1 - Road
2 - Wall
