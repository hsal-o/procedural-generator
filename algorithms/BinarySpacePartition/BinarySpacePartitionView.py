from AlgorithmView import AlgorithmView
from algorithms.BinarySpacePartition.BinarySpacePartitionController import BinarySpacePartitionController

class BinarySpacePartitionView(AlgorithmView):
    # Override implementation
    def initialize_attributes(self):
        self.controller = BinarySpacePartitionController(self)

        self.entry_iterations       = self.set_widget_id("entry_iterations")
        self.entry_start_x          = self.set_widget_id("entry_start_x")
        self.entry_start_y          = self.set_widget_id("entry_start_y")
        self.entry_end_x            = self.set_widget_id("entry_end_x")
        self.entry_end_y            = self.set_widget_id("entry_end_y")


    # Override implementation
    def create_section_configuration(self, root):
        self.mv.create_single_entry(root, "Max Iterations", self.entry_iterations, def_val=3) 
        self.mv.create_dual_entry(root, "Start (x, y)", self.entry_start_x, self.entry_start_y, 0, 0) 
        self.mv.create_dual_entry(root, "End (x, y)", self.entry_end_x, self.entry_end_y, self.mv.get_entry_width()-1, self.mv.get_entry_height()-1)

    # Override implementation
    def create_section_manipulation(self, root):
        return False

    # Override implementation
    def get_variables(self):
        self.variables["iterations"] = self.mv.get_entry_value_int(self.entry_iterations)
        self.variables["x1"] = self.mv.get_entry_value_int(self.entry_start_x)
        self.variables["y1"] = self.mv.get_entry_value_int(self.entry_start_y)
        self.variables["x2"] = self.mv.get_entry_value_int(self.entry_end_x)
        self.variables["y2"] = self.mv.get_entry_value_int(self.entry_end_y)