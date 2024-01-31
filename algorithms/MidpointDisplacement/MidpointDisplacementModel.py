import random
from math import ceil, floor
import cavegen.res.colors as colors
from AlgorithmModel import AlgorithmModel

class MidpointDisplacementModel(AlgorithmModel):
    #Override implementation
    def run(self, variables):
        points = self.generate_points(variables["x1"], variables["y1"], variables["x2"], variables["y2"], variables["magnitude"], variables["iterations"])
        self.connect_points(points, variables["stroke_thickness"], variables["do_random_thickness"])
        
    ################################################################################
    # Algorithm specific methods
    ################################################################################
    def generate_points(self, x1, y1, x2, y2, magnitude, step):
        if(step == 0):
            return [(x1, y1), (x2, y2)]
        
        height = len(self.grid)
        width = len(self.grid[0])
        
        midpoint_x = int((x1 + x2) / 2)
        midpoint_y = int((y1 + y2) / 2)

        new_midpoint_x = midpoint_x  + random.randint(-magnitude, magnitude)

        if(new_midpoint_x < 0):
            new_midpoint_x = -new_midpoint_x

        if(new_midpoint_x >= width):
            new_midpoint_x = width - (new_midpoint_x - width)

        if(midpoint_y >= height):
            midpoint_y = height - 1

        points_start = self.generate_points(x1, y1, new_midpoint_x, midpoint_y, magnitude, step-1)
        points_end = self.generate_points(new_midpoint_x, midpoint_y, x2, y2, magnitude, step-1)

        return points_start + [(new_midpoint_x, midpoint_y)] + points_end
    
    def connect_points(self, points, stroke_thickness, do_random_thickness):
        for i in range(len(points)-1):
            self.draw_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], stroke_thickness, do_random_thickness)
            
    def draw_line(self, x1, y1, x2, y2, stroke_thickness, do_random_thickness):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        if do_random_thickness:
            new_thickness = stroke_thickness + random.choice([0, 2])
        else:
            new_thickness = stroke_thickness

        while (x1 != x2) or (y1 != y2):
            x_thickness = new_thickness #- 1
            x_tt = ceil(x_thickness / 2)
            x_bt = floor(x_thickness / 2)

            y_thickness = stroke_thickness #- 1
            y_tt = ceil(y_thickness / 2)
            y_bt = floor(y_thickness / 2)

            for _x in range(x1 - x_tt, x1 + x_bt):
                for _y in range(y1 - y_tt, y1 + y_bt):
                    try:
                        if(_x >= 0 and _x < self.width and _y >= 0 and _y < self.height):
                            self.grid[_y][_x] = 0 # Air 
                            # self.grid[_x][_y] = colors.rgb_white
                    except:
                        print("caught exception: _x:", _x, ", _y:", _y)

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy


