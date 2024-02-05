import random
from math import ceil, floor
import cavegen.res.colors as colors
from AlgorithmModel import AlgorithmModel

class Room:
    def __init__(self, start_coord, end_coord):
        self.x1, self.y1 = start_coord
        self.x2, self.y2 = end_coord
        self.center_x = (self.x2 + self.x1) // 2
        self.center_y = (self.y2 + self.y1) // 2
        self.center_coord = (self.center_x, self.center_y)


class BinarySpacePartitionModel(AlgorithmModel):
    # Override implementation
    def run(self, variables):
        self.raw_rooms = []
        self.built_rooms = []
        
        self.side_left = 0
        self.side_top = 1
        self.side_right = 2
        self.side_bottom = 3

        self.min_width = variables["min_width"]
        self.min_height = variables["min_height"]
        self.hallway_stroke_thickness = variables["hallway_stroke_thickness"]

        self.generate_cut((variables["x1"], variables["y1"]),
                          (variables["x2"]+1, variables["y2"]+1),
                          0,
                          variables["iterations"],
                          variables["do_connect_rooms"])

    

    ################################################################################
    # Algorithm specific methods
    ################################################################################
    def generate_cut(self, start_coord, end_coord, iteration_count, max_iteration_count, do_connect_rooms):
        x1, y1 = start_coord
        x2, y2 = end_coord

        # if(iteration_count >= max_iteration_count):
        if(iteration_count >= max_iteration_count or
           x2 - x1 < self.min_width or
           y2 - y1 < self.min_height):
            
            raw_room = Room(start_coord, end_coord)
            return([self.generate_single_room(raw_room)])
        
        def cut_vertical(x1, y1, x2, y2):
            bound = (x2-x1) // 3
            m_x = random.randint(x1+bound, x2-bound)
            # m_x = (x2 + x1) // 2
            m_start_coord = (m_x, y1)
            m_end_coord = (m_x, y2)

            return m_start_coord, m_end_coord
        
        def cut_horizontal(x1, y1, x2, y2):
            bound = (y2-y1) // 3
            m_y = random.randint(y1+bound, y2-bound)
            # m_y = (y2 + y1) // 2
            m_start_coord = (x1, m_y)
            m_end_coord = (x2, m_y)

            return m_start_coord, m_end_coord
        
        width = x2-x1
        height = y2-y1
        if(width > height): # Vertical cut
            m_start_coord, m_end_coord = cut_vertical(x1, y1, x2, y2)

        elif(height > width): # Horizontal cut
            m_start_coord, m_end_coord = cut_horizontal(x1, y1, x2, y2)

        else: # Choose randomly
            cut_direction = random.choice([0,1])
            if(cut_direction == 0): # Vertical cut
                m_start_coord, m_end_coord = cut_vertical(x1, y1, x2, y2)
            elif(cut_direction == 1): # Horizontal cut
                m_start_coord, m_end_coord = cut_horizontal(x1, y1, x2, y2)
     
        alpha_rooms = self.generate_cut(start_coord, m_end_coord, iteration_count + 1, max_iteration_count, do_connect_rooms)
        beta_rooms = self.generate_cut(m_start_coord, end_coord, iteration_count + 1, max_iteration_count, do_connect_rooms)
        if(do_connect_rooms):
            self.conjoin_rooms(alpha_rooms, beta_rooms)

        return alpha_rooms + beta_rooms


    def conjoin_rooms(self, alpha_rooms, beta_rooms):
        def rooms_overlap_x_range(a_room, b_room):
            return max(a_room.x1, b_room.x1) <= min(a_room.x2, b_room.x2)
        
        def rooms_overlap_y_range(a_room, b_room):
            return max(a_room.y1, b_room.y1) <= min(a_room.y2, b_room.y2)

        room_seperation_distance = 2
        for a_room in alpha_rooms:
            for b_room in beta_rooms:
                # [b_room][a_room] connection
                # if(a_room.x1-1 == b_room.x2):
                if(b_room.x2 - a_room.x1 == room_seperation_distance):
                    if(rooms_overlap_y_range(a_room, b_room)):
                        self.connect_rooms(a_room, b_room, self.side_left)
                        return
                    
                # [b_room]
                # [a_room] connection
                # elif(a_room.y1-1 == b_room.y2):
                elif(b_room.y2 - a_room.y1 == room_seperation_distance):
                    if(rooms_overlap_x_range(a_room, b_room)):
                        self.connect_rooms(a_room, b_room, self.side_top)
                        return

                # [a_room][b_room] connection
                # elif(a_room.x2+1 == b_room.x1):
                elif(b_room.x1 - a_room.x2 == room_seperation_distance):
                    if(rooms_overlap_y_range(a_room, b_room)):
                        self.connect_rooms(a_room, b_room, self.side_right)
                        return
                    
                # [a_room]
                # [b_room] connection
                # elif(a_room.y2+1 == b_room.y1):
                elif(b_room.y1 - a_room.y2 == room_seperation_distance):
                    if(rooms_overlap_x_range(a_room, b_room)):
                        self.connect_rooms(a_room, b_room, self.side_bottom)
                        return
                
                else: # Rooms are not neighbors
                    continue

    def connect_rooms(self, room_1, room_2, side):
        if(side == self.side_left):
            room_1_coord = (room_1.x1, (room_1.y1+room_1.y2) // 2)
            room_2_coord = (room_2.x2, (room_2.y1+room_2.y2) // 2)

        elif(side == self.side_top):
            room_1_coord = ((room_1.x1+room_1.x2) // 2, room_1.y1)
            room_2_coord = ((room_2.x1+room_2.x2) // 2, room_2.y2)

        elif(side == self.side_right):
            room_1_coord = (room_1.x2, (room_1.y1+room_1.y2) // 2)
            room_2_coord = (room_2.x1, (room_2.y1+room_2.y2) // 2)

        elif(side == self.side_bottom):
            room_1_coord = ((room_1.x1+room_1.x2) // 2, room_1.y2)
            room_2_coord = ((room_2.x1+room_2.x2) // 2, room_2.y1)

        self.connect_points(room_1_coord, room_2_coord, stroke_thickness=self.hallway_stroke_thickness, do_random_thickness=False)


    def generate_single_room(self, room):
        # (x1, y1), (x2, y2) = room
        x1 = room.x1 + 1
        y1 = room.y1 + 1
        x2 = room.x2 - 1
        y2 = room.y2 - 1

        # If not randomized room sizes
        start_x = x1
        start_y = y1
        end_x = x2
        end_y = y2

        # bound_x = 1
        # bound_y = 1
        # start_x = random.randint(x1, x1+bound_x)
        # start_y = random.randint(y1, y1+bound_y)
        # end_x = random.randint(x2-bound_x, x2)
        # end_y = random.randint(y2-bound_y, y2)

        # Paint in rooms
        for _x in range(start_x, end_x):
            for _y in range(start_y, end_y):
                self.grid[_y][_x] = 0

        # self.built_rooms.append(Room((start_x, start_y), (end_x, end_y)))
        return Room((start_x, start_y), (end_x, end_y))
        

    def connect_points(self, start_coord, end_coord, stroke_thickness, do_random_thickness):
        x1, y1 = start_coord
        x2, y2 = end_coord

        self.draw_line(x1, y1, x2, y2, stroke_thickness, do_random_thickness)

            
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
                    except:
                        print("caught exception: _x:", _x, ", _y:", _y)

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        # Paint last cell
        if(stroke_thickness > 0):
            self.grid[y2-1][x2-1] = 0

