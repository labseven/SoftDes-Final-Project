"""
World:
Holds the map.
"""
import numpy as np

class World():
    def __init__(self, size):
        self.world_map = np.zeros(size)
