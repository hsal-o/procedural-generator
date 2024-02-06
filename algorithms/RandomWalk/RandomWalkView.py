from AlgorithmView import AlgorithmView
from algorithms.RandomWalk.RandomWalkController import RandomWalkController

class RandomWalkView(AlgorithmView):
    # Override implementation
    def initialize_attributes(self):
        self.controller = RandomWalkController(self)

        # Entries
        self.entry_num_walkers = self.set_widget_id("entry_num_walkers")
        self.entry_steps = self.set_widget_id("entry_steps")
        self.entry_stroke_thickness = self.set_widget_id("entry_stroke_thickness")
        self.entry_start_x = self.set_widget_id("entry_start_x")
        self.entry_start_y = self.set_widget_id("entry_start_y")

        # Checkboxes
        self.cbox_randomize_start = self.set_widget_id("cbox_randomize_start")
        # self.cbox_randomize_stroke_thickness = self.set_widget_id("cbox_randomize_stroke_thickness")

    # Override implementation
    def create_section_configuration(self, root):
        self.mv.create_single_entry(root, "# of Walkers", self.entry_num_walkers, def_val=10)
        self.mv.create_single_entry(root, "Steps", self.entry_steps, def_val=100)
        self.mv.create_single_entry(root, "Stroke Thickness", self.entry_stroke_thickness, def_val=2)        
        self.mv.create_dual_entry(root, "Start (x, y)", self.entry_start_x, self.entry_start_y, self.mv.get_entry_width()//2, self.mv.get_entry_height()//2) 

        self.mv.create_single_checkbox(root, "Randomize Start Position", self.cbox_randomize_start, def_val=False)
        # self.mv.create_single_checkbox(root, "Randomize Stroke Thickness", self.cbox_randomize_stroke_thickness, def_val=False)


    # Override implementation
    def get_variables(self):
        self.variables["num_walkers"] = self.mv.get_entry_value_int(self.entry_num_walkers)
        self.variables["steps"] = self.mv.get_entry_value_int(self.entry_steps)
        self.variables["stroke_thickness"] = self.mv.get_entry_value_int(self.entry_stroke_thickness)        
        self.variables["start_x"] = self.mv.get_entry_value_int(self.entry_start_x)
        self.variables["start_y"] = self.mv.get_entry_value_int(self.entry_start_y)

        self.variables["do_random_start"] = self.mv.get_entry_value_bool(self.cbox_randomize_start)
        # self.variables["do_random_thickness"] = self.mv.get_entry_value_bool(self.cbox_randomize_stroke_thickness)
