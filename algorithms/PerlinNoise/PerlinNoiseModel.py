import random
from math import ceil, floor
import cavegen.res.colors as colors
from AlgorithmModel import AlgorithmModel
from perlin_noise import PerlinNoise

class PerlinNoiseModel(AlgorithmModel):
    # Override implementation
    def run(self, variables):
        self.lower_bound = variables["lower_bound"]
        self.upper_bound = variables["upper_bound"]

        self.generate_perlin_noise(variables["width"], 
                                   variables["height"], 
                                   variables["octave"],
                                   variables["show_perlin_noise"])
        
    # Override parent
    def color_grid(self, grid):
        # TO-DO : Refactor original grid to follow scheme
        color_grid = [[None for _ in range(self.width)] for _ in range(self.height)]

        for _y in range(self.height):
            for _x in range(self.width):
                # Map Perlin noise values to the range [0, 255]
                color_value = int((grid[_y][_x] + 1) * 127.5)

                # Set RGB values based on the color_value
                color = [color_value, color_value, color_value]
                color_grid[_y][_x] = color

        return color_grid

    ################################################################################
    # Algorithm specific methods
    ################################################################################
    def generate_perlin_worm_point(self, x, y, perlin_noise_value):
        if(perlin_noise_value > self.lower_bound and perlin_noise_value < self.upper_bound):
            self.grid[y][x] = 1 # NonSolid
        else:
            self.grid[y][x] = -1 # Solid

    def generate_perlin_noise(self, width, height, octave, show_perlin_noise):

        noise = PerlinNoise(octaves=octave, seed=self.seed)
        for y in range(0, height):
            for x in range(0, width):
                perlin_noise_value = noise([x/(width*2), y/(height*2)])

                if(not show_perlin_noise):
                    self.generate_perlin_worm_point(x, y, perlin_noise_value)
                else:
                    self.grid[y][x] = perlin_noise_value

                # if(perlin_noise > lower_bound and perlin_noise < upper_bound):
                #     self.grid[y][x] = 0

        # self.grid = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
