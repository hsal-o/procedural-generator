import numpy as np
import random
from math import ceil, floor
import cavegen.res.colors as colors
from AlgorithmModel import AlgorithmModel
from perlin_noise import PerlinNoise

class PerlinWormsModel(AlgorithmModel):
    def __init__(self):
        super().__init__()
        self.nonsolid = 1
        self.solid = -1

    # Override implementation
    def run(self, variables):
        self.lower_bound = variables["lower_bound"]
        self.upper_bound = variables["upper_bound"]

        self.generate_perlin_noise(variables["width"], 
                                   variables["height"], 
                                   variables["octave"],
                                   variables["show_perlin_noise"])
        
        if(not variables["show_perlin_noise"] and variables["apply_cellular_automata"]):
            self.apply_cellular_automata()
        
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
    
    def get_binary_grid(self):
        binary_grid = [[None for _ in range(self.width)] for _ in range(self.height)]

        for _y in range(self.height):
            for _x in range(self.width):
                if(self.grid[_y][_x] == -1):
                    binary_grid[_y][_x] = 1
                elif(self.grid[_y][_x] == 1):
                    binary_grid[_y][_x] = 0

        return binary_grid

    ################################################################################
    # Algorithm specific methods
    ################################################################################
    def generate_perlin_worm_point(self, x, y, perlin_noise_value):
        if(perlin_noise_value > self.lower_bound and perlin_noise_value < self.upper_bound):
            self.grid[y][x] = self.nonsolid # NonSolid
        else:
            self.grid[y][x] = self.solid # Solid

    def generate_perlin_noise(self, width, height, octave, show_perlin_noise):
        noise = PerlinNoise(octaves=octave, seed=self.seed)
        for y in range(0, height):
            for x in range(0, width):
                normalized_x = x / (width)
                normalized_y = y / (height)
                perlin_noise_value = noise([normalized_x, normalized_y])

                if not show_perlin_noise:
                    self.generate_perlin_worm_point(x, y, perlin_noise_value)
                else:
                    self.grid[y][x] = perlin_noise_value

    def apply_cellular_automata(self):
        border_size = 4
        nonsolid_odds = 0.0

        # Randomize borders
        for y in range(0, self.height):
            for x in range(0, self.width):
                if(y >= border_size and y <= self.height-border_size and
                   x >= border_size and x <= self.width-border_size):
                    continue

                if(self.grid[y][x] == 1):
                    nonsolid_odds = 0.8
                else:
                    nonsolid_odds = 0.6

                # Calculate chance
                chance = random.random()
                # Determine if cell should be nonsolid
                self.grid[y][x] = 1 if chance <= nonsolid_odds else -1

        # Apply Cellular automata
        for _ in range(0, 10):
            self.generate_iteration(4, 3)


    def count_solid_neighbors(self, y, x):
        count = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                # Skip calling cell
                if(dy == 0 and dx == 0):
                    continue

                # Check if neighbor is in bounds
                ny = y + dy
                nx = x + dx
                if(ny < 0 or nx < 0 or ny >= self.height or nx >= self.width):
                    continue

                # Count solid neighbors
                if(self.grid[ny][nx] == self.solid):
                    count += 1

        return count


    def generate_iteration(self, num_to_turn_solid, num_to_turn_nonsolid):
        new_grid = [[self.grid[y][x] for x in range(self.width)] for y in range(self.height)]
        # Set the border elements to -1
        for y in range(self.height):
            new_grid[y][0] = self.solid  # first column
            new_grid[y][-1] = self.solid # last column

        for x in range(self.width):
            new_grid[0][x] = self.solid  # first row
            new_grid[-1][x] = self.solid  # last row

        border_size = 5
        for y in range(0, self.height):
            for x in range(0, self.width):
                # Exclude border cells
                if(y == 0 or x == 0 or y == self.height-1 or x == self.width-1):
                    new_grid[y][x] = self.solid # Turn solid automatically
                    continue

                if(y >= border_size and y <= self.height-border_size and
                   x >= border_size and x <= self.width-border_size):
                    continue
                
                num_solid_neighbors = self.count_solid_neighbors(y, x)

                # If current cell is Solid
                if(self.grid[y][x] == self.solid):
                    if(num_solid_neighbors < num_to_turn_nonsolid):
                        # Cell turns nonsolid due to under/overpopulation
                        new_grid[y][x] = self.nonsolid
                    else :
                        # Cell remains solid
                        new_grid[y][x] = self.solid
                
                # If current cell is NonSolid
                elif(self.grid[y][x] == self.nonsolid):
                    if(num_solid_neighbors > num_to_turn_solid):
                        # Cell turns solid due to reproduction
                        new_grid[y][x] = self.solid
                    else:
                        # Cell remains nonsolid
                        new_grid[y][x] = self.nonsolid

        self.grid = new_grid


