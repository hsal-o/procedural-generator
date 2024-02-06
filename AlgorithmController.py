from abc import ABC, abstractmethod 
import random
import matplotlib.pyplot as plt

class AlgorithmController(ABC):
    def __init__(self, view):
        # Initialize seed
        self.seed = self.get_random_seed()

        # Initialize attributes
        self.model = None
        self.view = None
        self.initialize_attributes(view)

        # Initialize helper variables
        self.has_flipped_x = False
        self.has_flipped_y = False

    @abstractmethod
    def initialize_attributes(self, view):
        # Initialize model
        # self.model = AlgorithmModel()

        # Initialize view
        # self.view = view
        pass

    def initialize(self, variables):
        self.variables = variables
        self.model.set_grid(self.variables["width"], self.variables["height"])
         
    def run(self, is_seed_provided):
        # FIX
        if is_seed_provided:
            self.seed = self.view.get_entry_seed()
        else:
            self.seed = self.get_random_seed()

        self.view.set_entry_seed(self.seed)

        self.model.generate(self.seed, self.variables)

    def export_grid(self, algorithm_name):
        self.model.export_grid(algorithm_name)

    def import_grid(self):

        if(self.model.import_grid()):
            self.view.set_entry_seed(self.model.get_seed())
            self.view.set_entry_value("entry_width", self.model.get_width())
            self.view.set_entry_value("entry_height", self.model.get_height())
            self.view.update_grid_figure(imported=True)

            self.view.mv.toggle_section_grid_manipulation(True)


    ################################################################################
    # Getters
    ################################################################################
    def get_random_seed(self):
        return random.randint(0, 2**32 - 1)
    
    def get_grid_figure(self, flip_x=False, flip_y=False, imported=False):
        if(not flip_x and not flip_y):
            self.has_flipped_x = False
            self.has_flipped_y = False

        figure_size = 4
        # Create Matplotlib figure and plot
        figure, ax = plt.subplots(figsize=(figure_size, figure_size))
        ax.imshow(self.model.get_grid())

        if(flip_x):
            self.has_flipped_x = not self.has_flipped_x
            if(self.has_flipped_x):
                ax.invert_xaxis()

        if(flip_y):
            self.has_flipped_y = not self.has_flipped_y
            if(self.has_flipped_y):
                ax.invert_yaxis()

        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        figure_name = self.view.get_name() if not imported else "Imported Grid"
        ax.set_title(f"{figure_name}")

        plt.close(figure)

        return figure

    def get_raw_grid_figure(self):
        return self.model.get_grid()
    