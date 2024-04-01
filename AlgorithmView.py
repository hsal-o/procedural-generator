from abc import ABC, abstractmethod 

class AlgorithmView(ABC):

    def __init__(self, main_view, full_name):
        self.mv = main_view
        self.variables = {}
        self.full_name = full_name
        self.initialize_attributes()

    @abstractmethod
    def initialize_attributes(self):
        # Initialize controller
        # self.controller = AlgorithmController(self)

        # Initialize name
        # self.name = "Algorithm"

        # Initialize nickname
        # self.nickname = "Algo"

        # Initialize widget variable names
        # self.label_implement = "label_implement"
        pass

    def set_widget_id(self, name):
        return f"{self.full_name}_{name}"

    ################################################################################
    # Getters
    ################################################################################
    def get_entry_seed(self):
        return self.mv.get_entry_seed()
    
    def get_name(self):
        return self.full_name
    
    def get_nickname(self):
        return self.nickname
    
    def get_raw_grid_figure(self):
        return self.controller.get_raw_grid_figure()
    
    ################################################################################
    # Setters
    ################################################################################
    def set_entry_seed(self, seed):
        self.mv.set_entry_seed(seed)

    def update_grid_figure(self, imported=False):
        self.mv.show_output_grid(self.controller.get_grid_figure(imported=imported))

    def set_entry_value(self, entry, value):
        self.mv.set_entry_value(entry, value)

    ################################################################################
    # MainView Button on_click implementations
    ################################################################################
    def button_flip_x_on_click(self):
        self.mv.show_output_grid(self.controller.get_grid_figure(flip_x=True))

    def button_flip_y_on_click(self):
        self.mv.show_output_grid(self.controller.get_grid_figure(flip_y=True))

    def generate_button_on_click(self, is_seed_provided):
        self.generate_output_grid(is_seed_provided)
        self.mv.show_output_grid(self.controller.get_grid_figure())

    def generate_with_seed_button_on_click(self):
        self.generate_output_grid(is_seed_provided=True)
        self.mv.show_output_grid(self.controller.get_grid_figure())

    ################################################################################
    # Section Creation
    ################################################################################
    @abstractmethod
    def create_section_configuration(self, root):
        # label_missing_implement = "label_missing_implement"
        # self.mv.create_single_label(root, "Implement me!", label_missing_implement)
        pass

    def create_section_manipulation(self, root):
        # label_missing_implement = "label_missing_implement"
        # self.mv.create_single_label(root, "Implement me!", label_missing_implement)
        return False
    
    def create_section_presets(self, root):
        return False

    ################################################################################
    # Generation
    ################################################################################
    @abstractmethod
    def get_variables(self):
        # self.variables["magnitude"]  = self.mv.get_entry_value_int(self.entry_magnitude)
        # self.variables["variance"] = self.mv.get_entry_value_int(self.entry_variance)
        pass

    def generate_output_grid(self, is_seed_provided):
        # Get generic variables
        self.variables["width"]  = self.mv.get_entry_width()
        self.variables["height"] = self.mv.get_entry_height()

        # Get specific variables
        self.get_variables()

        # Initialize and run algorithm
        self.controller.initialize(self.variables)
        self.controller.run(is_seed_provided)

    ################################################################################
    # Button On Click Implementations
    ################################################################################
    def button_export_on_click(self, algorithm_name):
        self.controller.export_grid(algorithm_name)

    def button_import_on_click(self):
        self.controller.import_grid()