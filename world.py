"""
World:
Holds the map.
"""
import numpy as np

class World():
    def __init__(self, size):
        print (size[1])
        self.world_map = np.zeros(size)
