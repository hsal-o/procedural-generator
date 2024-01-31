from AlgorithmView import AlgorithmView
from algorithms.MidpointDisplacement.MidpointDisplacementController import MidpointDisplacementController

class MidpointDisplacementView(AlgorithmView):
    # Override implementation
    def initialize_attributes(self):
        self.controller = MidpointDisplacementController(self)

        # Entries
        self.entry_magnitude        = self.set_widget_id("entry_magnitude")
        self.entry_iterations       = self.set_widget_id("entry_iterations")
        self.entry_stroke_thickness = self.set_widget_id("entry_stroke_thickness")
        self.entry_start_x          = self.set_widget_id("entry_start_x")
        self.entry_start_y          = self.set_widget_id("entry_start_y")
        self.entry_end_x            = self.set_widget_id("entry_end_x")
        self.entry_end_y            = self.set_widget_id("entry_end_y")

        # Checkboxes
        self.cbox_randomize_stroke_thickness = self.set_widget_id("cbox_randomize_stroke_thickness")

    # Override implementation
    def create_section_configuration(self, root):
        # Add single Entries
        self.mv.create_single_entry(root, "Magnitude",        self.entry_magnitude,         def_val=6) # 16
        self.mv.create_single_entry(root, "Iterations",       self.entry_iterations,        def_val=5) # 5
        self.mv.create_single_entry(root, "Stroke Thickness", self.entry_stroke_thickness,  def_val=3) # 3

        # Add double entries
        self.mv.create_dual_entry(root, "Start (x, y)", self.entry_start_x, self.entry_start_y, 0, 0) 
        self.mv.create_dual_entry(root, "End (x, y)",   self.entry_end_x, self.entry_end_y, self.mv.get_entry_width()-1, self.mv.get_entry_height()-1)

        # Add Checkboxes
        self.mv.create_single_checkbox(root, "Randomize Line Thickess", self.cbox_randomize_stroke_thickness, True)

        # print(f"Created section for {self.full_name}!")

    # Override implementation
    def create_section_manipulation(self, root):
        return False

    # Override implementation
    def get_variables(self):
        self.variables["magnitude"]              = self.mv.get_entry_value_int(self.entry_magnitude)
        self.variables["iterations"]             = self.mv.get_entry_value_int(self.entry_iterations)
        self.variables["stroke_thickness"]       = self.mv.get_entry_value_int(self.entry_stroke_thickness)
        self.variables["do_random_thickness"]    = self.mv.get_entry_value_bool(self.cbox_randomize_stroke_thickness)

        self.variables["x1"] = self.mv.get_entry_value_int(self.entry_start_x)
        self.variables["y1"] = self.mv.get_entry_value_int(self.entry_start_y)
        self.variables["x2"] = self.mv.get_entry_value_int(self.entry_end_x)
        self.variables["y2"] = self.mv.get_entry_value_int(self.entry_end_y)
