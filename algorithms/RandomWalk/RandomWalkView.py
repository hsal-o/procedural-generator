from AlgorithmView import AlgorithmView
from algorithms.RandomWalk.RandomWalkController import RandomWalkController

class RandomWalkView(AlgorithmView):
    # Override implementation
    def initialize_attributes(self):
        self.controller = RandomWalkController(self)

        self.label_implement_me = self.set_widget_id("label_implement_me!")

        self.entry_steps = self.set_widget_id("entry_steps")
        self.entry_start_x = self.set_widget_id("entry_start_x")
        self.entry_start_y = self.set_widget_id("entry_start_y")

    # Override implementation
    def create_section_configuration(self, root):
        self.mv.create_single_label(root, "Implement me!", self.label_implement_me)

        self.mv.create_single_entry(root, "Steps", self.entry_steps, def_val=100)
        self.mv.create_dual_entry(root, "Start (x, y)", self.entry_start_x, self.entry_start_y, self.mv.get_entry_width()//2, self.mv.get_entry_height()//2) 

    # Override implementation
    def create_section_manipulation(self, root):
        return False

    # Override implementation
    def get_variables(self):
        self.variables["steps"] = self.mv.get_entry_value_int(self.entry_steps)
        self.variables["start_x"] = self.mv.get_entry_value_int(self.entry_start_x)
        self.variables["start_y"] = self.mv.get_entry_value_int(self.entry_start_y)