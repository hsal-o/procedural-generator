import random
from math import ceil, floor
import cavegen.res.colors as colors
from AlgorithmModel import AlgorithmModel

class RandomWalkModel(AlgorithmModel):
    # Override implementation
    def run(self, variables):
        self.generate_steps(variables["steps"], variables["start_x"], variables["start_y"])
    
    ################################################################################
    # Algorithm specific methods
    ################################################################################
    def generate_steps(self, steps, start_x, start_y):
        self.grid[start_y][start_x] = 0
