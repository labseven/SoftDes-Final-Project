"""
World:
Holds the map.
"""
import numpy as np

class World():
    def __init__(self, size):
        self.world_map = np.zeros(size)

        # Quick wall for testing
        for i in range(size[0]):
            self.world_map[i][0] = 1
        print(self.world_map)
