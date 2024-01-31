import random
from math import ceil, floor
import cavegen.res.colors as colors
from AlgorithmModel import AlgorithmModel

class CellularAutomataModel(AlgorithmModel):
    # Override implementation
    def run(self, variables):
        self.generate_initial_grid(variables["nonsolid_odds"])
        
        for _ in range(0, variables["iterations"]):
            self.generate_iteration(variables["num_to_turn_solid"], variables["num_to_turn_nonsolid"])
    
    ################################################################################
    # Algorithm specific methods
    ################################################################################
    def generate_initial_grid(self, nonsolid_odds):
        for y in range(0, self.height):
            for x in range(0, self.width):
                # Exclude border cells
                if(y == 0 or x == 0 or y == self.height-1 or x == self.width-1):
                    self.grid[y][x] = 1 # Turn solid automatically
                    continue
                
                # Calculate chance
                chance = random.random()
                # Determine if cell should be nonsolid
                self.grid[y][x] = 0 if chance <= nonsolid_odds else 1

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
                if(self.grid[ny][nx] == 1):
                    count += 1

        return count

    def generate_iteration(self, num_to_turn_solid, num_to_turn_nonsolid):
        new_grid = [[None for _ in range(self.width)] for _ in range(self.height)]

        for y in range(0, self.height):
            for x in range(0, self.width):
                # Exclude border cells
                if(y == 0 or x == 0 or y == self.height-1 or x == self.width-1):
                    new_grid[y][x] = 1 # Turn solid automatically
                    continue
                
                num_solid_neighbors = self.count_solid_neighbors(y, x)

                # If current cell is Solid
                if(self.grid[y][x] == 1):
                    if(num_solid_neighbors < num_to_turn_nonsolid):
                        # Cell turns nonsolid due to under/overpopulation
                        new_grid[y][x] = 0
                    else :
                        # Cell remains solid
                        new_grid[y][x] = 1
                
                # If current cell is NonSolid
                elif(self.grid[y][x] == 0):
                    if(num_solid_neighbors > num_to_turn_solid):
                        # Cell turns solid due to reproduction
                        new_grid[y][x] = 1
                    else:
                        # Cell remains nonsolid
                        new_grid[y][x] = 0

        self.grid = new_grid
