from abc import ABC, abstractmethod 
import os.path
from datetime import datetime
from tkinter import messagebox, simpledialog
from tkinter.filedialog import askopenfilename
import numpy as np
import random
import cavegen.res.colors as colors

class AlgorithmModel(ABC):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.grid = []
        self.seed = 0

    ################################################################################
    # Getters
    ################################################################################
    def get_grid(self):
        color_grid = self.color_grid(self.grid)
        return np.array(color_grid, dtype=np.uint8)

    def get_binary_grid(self):
        return np.array(self.grid)

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height

    def get_seed(self):
        return self.seed

    ################################################################################
    # Setters
    ################################################################################
    def set_grid(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width)] for _ in range(height)]

    ################################################################################
    # Generation
    ################################################################################
    def generate(self, seed, variables):
        random.seed(seed)
        self.seed = seed
        self.run(variables)

    @abstractmethod
    def run(self, variables):
        pass

    def color_grid(self, grid):
        # TO-DO : Refactor original grid to follow scheme
        color_grid = [[None for _ in range(self.width)] for _ in range(self.height)]

        for _y in range(self.height):
            for _x in range(self.width):
                if(grid[_y][_x] == 0):
                    color_grid[_y][_x] = colors.rgb_white
                elif(grid[_y][_x] == 1):
                    color_grid[_y][_x] = colors.rgb_black

        return color_grid

    def export_grid(self, algorithm_name):
        # Get the current date and time
        current_datetime = datetime.now()
        time_stamp = current_datetime.strftime(f"%Y-%m-%d_%H-%M-%S")
        default_file_name = f"{time_stamp}_{algorithm_name}"

        user_input = simpledialog.askstring(title='Export Grid', prompt='Enter a File name', initialvalue=default_file_name)
        
        # User closed out so break out
        if(user_input == None):
            return
        
        if(user_input == ""):
            user_input = default_file_name

        file_name = f"{user_input}.grid"

        try:
            # Check if file exists
            path = f"grids/{file_name}"
            if(os.path.isfile(path)):
                # File with given name already exists
                if(messagebox.askyesno(title="Overwrite File?", message=f"A file already exists named \'{file_name}\'\nDo you want to overwrite?") == False):
                    return

            # Open file
            file = open(path, "w")

            file.write(f"Width: {self.width}\n")
            file.write(f"Height: {self.height}\n")
            file.write(f"Seed: {self.seed}\n")
            
            for row in self.grid:
                binary_row = ''.join(map(str, row))

                # TO-DO: Better compress binary row representation
                # hexadecimal_row = hex(int(binary_row, 2))

                file.write(f"{binary_row}\n")

            messagebox.showinfo("Success", f"Exported Grid under file\n{file_name}")
        except:
            messagebox.showerror("Error", f"Could not export grid")

        file.close()


    def import_grid(self):
        file_name = askopenfilename()

        try:
            with open(f"{file_name}", "r") as file:
                width  = int(file.readline().strip().split()[1])
                height  = int(file.readline().strip().split()[1])
                seed  = int(file.readline().strip().split()[1])

                grid = []
                for line in file:
                    row = [int(digit) for digit in line.strip()]
                    grid.append(row)

                self.width = width
                self.height = height
                self.seed = seed
                self.grid = grid

            return True
        
        except:
            messagebox.showerror("Error", f"Could not import grid")
            return False
        


        
