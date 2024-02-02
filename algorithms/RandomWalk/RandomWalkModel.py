import random
from math import ceil, floor
import cavegen.res.colors as colors
from AlgorithmModel import AlgorithmModel

class RandomWalkModel(AlgorithmModel):
    # Override implementation
    def run(self, variables):
        for _ in range(variables["num_walkers"]):
            if(variables["do_random_start"]):
                start_x = random.randint(0, self.width-1)
                start_y = random.randint(0, self.height-1)
            else:
                start_x = variables["start_x"]
                start_y = variables["start_y"]

            self.generate_steps(variables["steps"], variables["stroke_thickness"], start_x, start_y)
            # self.generate_steps(variables["steps"], variables["stroke_thickness"], variables["do_random_thickness"], start_x, start_y)
    
    ################################################################################
    # Algorithm specific methods
    ################################################################################
    def paint_step(self, stroke_thickness, x, y):
        # if do_random_thickness:
        #     new_thickness = stroke_thickness + random.choice([0, 1])
        # else:
        #     new_thickness = stroke_thickness

        x_tt = ceil(stroke_thickness / 2)
        x_bt = floor(stroke_thickness / 2)

        y_tt = ceil(stroke_thickness / 2)
        y_bt = floor(stroke_thickness / 2)

        for _x in range(x - x_tt, x + x_bt):
            for _y in range(y - y_tt, y + y_bt):
                if(_x >= 0 and _x < self.width and _y >= 0 and _y < self.height):
                    self.grid[_y][_x] = 0

    def generate_steps(self, steps, stroke_thickness, start_x, start_y):
        curr_x = start_x
        curr_y = start_y
        self.paint_step(stroke_thickness, curr_x, curr_y)
        for _ in range(0, steps-1):
            prev_x = curr_x
            prev_y = curr_y

            next_dir = random.randint(0, 3)
            if(next_dir == 0): # North
                curr_y -= 1
            elif(next_dir == 1): # East
                curr_x += 1
            elif(next_dir == 2): # South
                curr_y += 1
            elif(next_dir == 3): # West
                curr_x -= 1

            if(curr_x < 0 or curr_x >= self.width):
                curr_x = prev_x

            if(curr_y < 0 or curr_y >= self.height):
                curr_y = prev_y

            # # Avoid redundant painting
            if(curr_x == prev_x and curr_y == prev_y):
                continue

            self.paint_step(stroke_thickness, curr_x, curr_y)



