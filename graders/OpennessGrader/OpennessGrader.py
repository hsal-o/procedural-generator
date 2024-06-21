import numpy as np
import math
import copy
from ResourceManager import ResourceManager

class OpennessGrader:

    class Cell:
        def __init__(self, state, value):
            self.state = state
            self.value = value

    def get_solid_neighbor_value(self, grid, i, j):
        
        for _i in range(i-1, i+2):
            for _j in range(j-1, j+2):
                if _i == i and _j == j:
                    continue

                if(_i < 0 or _i >= len(grid)):
                    return -2

                if(_j < 0 or _j >= len(grid[0])):
                    return -2

                if(grid[_i][_j].state == 1):
                    return grid[_i][_j].value + 1
                
        return -1

    def get_value_counts(self, grid):
        value_counts = {}
        i = 1
        while(True):
            num_cells_with_value_i = np.sum([cell.value == i for row in grid for cell in row])
            if (num_cells_with_value_i == 0):
                break
            value_counts[i] = num_cells_with_value_i
            i += 1

        return value_counts

    def get_average(self, dictionary):
        weighted_sum = 0
        total_sum = 0
        for key in dictionary:
            # print(f"{dictionary[key]} cells have value {key}")
            weighted_sum += key * dictionary[key]
            total_sum += dictionary[key]
        average = weighted_sum / total_sum

        # return round(average, ResourceManager().FLOAT_PRECISION)
        return average

    def get_median(self, dictionary):
        # Seems to not gie right answers
        sorted_keys = sorted(dictionary.keys())
        num_total = sum(dictionary.values())
        
        # Get median position(s), (2 positions if num_total is even, else 1 position)
        if num_total % 2 == 0: # Even
            median_pos = [num_total / 2]
        elif num_total % 2 == 1: # Odd
            median_pos = [(num_total / 2) - 1, (num_total / 2)]

        # Use "Leap Frog" technique to find median value(s) faster
        cumalitive_index = 0
        median_values = []
        for key in sorted_keys:
            cumalitive_index += dictionary[key]
            
            for i in range(len(median_pos)-1, -1, -1):
                if cumalitive_index >= median_pos[i]:
                    median_pos.pop(i)
                    median_values.append(key)

        # Calculate true median (Important if num_total is even)
        total_sum = 0
        for i in range(len(median_values)):
            total_sum += median_values[i]
        median = total_sum / len(median_values)

        # return round(median, ResourceManager().FLOAT_PRECISION)
        return median
        
    def get_score(self, image_path, orig_grid):
        # Create empty grid
        grid = np.empty_like(orig_grid, dtype=object)

        # Initialize heat-map grid
        for i in range(0, len(orig_grid)):
            for j in range(0, len(orig_grid[0])): 
                state = orig_grid[i][j]
                
                # If solid
                if(state == 1):
                    # Set cell to solid with value of 0
                    grid[i][j] = self.Cell(state, 0)
                elif(state == 0):
                    # Set cell to nonsolid with uninitialized value (-1)
                    grid[i][j] = self.Cell(state, -1)

        # While nonsolids exist in the grid
        while any(cell.state == 0 for row in grid for cell in row):
            # Keep track of cells we update for future use
            updated_cells = []
            
            # Loop through grid
            for i in range(0, len(grid)):
                for j in range(0, len(grid[0])):
                    # If cell is an uninitialized nonsolid 
                    if(grid[i][j].state == 0 and grid[i][j].value == -1):

                        # Calculate value depending on solid neighbors
                        new_val = self.get_solid_neighbor_value(grid, i, j)

                        # If new_val is valid
                        if(new_val > 0):
                            # Set Cell to new value and add cell to list
                            grid[i][j].value = new_val
                            updated_cells.append(grid[i][j])
                        elif(new_val == -2): # Neighbor is out of range
                            # Set Cell value to 1 and add cell to list
                            grid[i][j].value = 1
                            updated_cells.append(grid[i][j])

            # Turn every updated cell into a solid
            for cell in updated_cells:
                cell.state = 1

        # Count Cell value occurences
        value_counts = self.get_value_counts(grid)

        # Get total number of nonsolid
        num_nonsolid_total = sum(value_counts.values())
        if(num_nonsolid_total == 0): return 0.0

        # Get number of nonsolids with value > 1
        num_nonsolid_desired = sum(value for key, value in value_counts.items() if key > 1)

        # Calculate score
        score = (num_nonsolid_desired / num_nonsolid_total)
        
        # return round(score, ResourceManager().FLOAT_PRECISION)
        return score


