from AlgorithmView import AlgorithmView
from algorithms.BinarySpacePartition.BinarySpacePartitionController import BinarySpacePartitionController

class BinarySpacePartitionView(AlgorithmView):
    # Override implementation
    def initialize_attributes(self):
        self.controller = BinarySpacePartitionController(self)

        # Entries
        self.entry_iterations       = self.set_widget_id("entry_iterations")
        self.entry_min_width       = self.set_widget_id("entry_min_width")
        self.entry_min_height       = self.set_widget_id("entry_min_height")
        self.entry_start_x          = self.set_widget_id("entry_start_x")
        self.entry_start_y          = self.set_widget_id("entry_start_y")
        self.entry_end_x            = self.set_widget_id("entry_end_x")
        self.entry_end_y            = self.set_widget_id("entry_end_y")
        self.entry_hallway_stroke_thickness = self.set_widget_id("entry_hallway_stroke_thickness")

        # Checkboxes
        self.cbox_connect_rooms = self.set_widget_id("cbox_connect_rooms")

    # Override implementation
    def create_section_configuration(self, root):
        # Add Entries
        self.mv.create_single_entry(root, "Max Iterations", self.entry_iterations, def_val=3) 
        self.mv.create_single_entry(root, "Mininum Cut Width", self.entry_min_width, def_val=8)
        self.mv.create_single_entry(root, "Mininum Cut Height", self.entry_min_height, def_val=8)
        self.mv.create_dual_entry(root, "Start (x, y)", self.entry_start_x, self.entry_start_y, 0, 0) 
        self.mv.create_dual_entry(root, "End (x, y)", self.entry_end_x, self.entry_end_y, self.mv.get_entry_width()-1, self.mv.get_entry_height()-1)
        self.mv.create_single_entry(root, "Connecting Thickness", self.entry_hallway_stroke_thickness, def_val=2)

        # Add Checkboxes
        self.mv.create_single_checkbox(root, "Connect Rooms", self.cbox_connect_rooms, def_val=True)


    # Override implementation
    def get_variables(self):
        # Entries
        self.variables["iterations"] = self.mv.get_entry_value_int(self.entry_iterations)
        self.variables["min_width"] = self.mv.get_entry_value_int(self.entry_min_width)
        self.variables["min_height"] = self.mv.get_entry_value_int(self.entry_min_height)
        self.variables["x1"] = self.mv.get_entry_value_int(self.entry_start_x)
        self.variables["y1"] = self.mv.get_entry_value_int(self.entry_start_y)
        self.variables["x2"] = self.mv.get_entry_value_int(self.entry_end_x)
        self.variables["y2"] = self.mv.get_entry_value_int(self.entry_end_y)
        self.variables["hallway_stroke_thickness"] = self.mv.get_entry_value_int(self.entry_hallway_stroke_thickness)

        # Checkboxes
        self.variables["do_connect_rooms"] = self.mv.get_entry_value_bool(self.cbox_connect_rooms)

