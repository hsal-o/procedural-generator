from AlgorithmView import AlgorithmView
from algorithms.CellularAutomata.CellularAutomataController import CellularAutomataController

class CellularAutomataView(AlgorithmView):
    # Override implementation
    def initialize_attributes(self):
        self.controller = CellularAutomataController(self)

        # Widgets
        self.entry_iterations = self.set_widget_id("entry_iterations")
        self.entry_nonsolid_odds = self.set_widget_id("entry_nonsolid_odds")

        self.label_conversion_info = self.set_widget_id("label_conversion_info")

        self.entry_num_to_turn_solid = self.set_widget_id("entry_num_to_turn_solid")
        self.entry_num_to_turn_nonsolid = self.set_widget_id("entry_num_to_turn_nonsolid")

        self.button_iteration = self.set_widget_id("button_iteration")


    # Override implementation
    def create_section_configuration(self, root):
        
        self.mv.create_single_entry(root, "Iterations", self.entry_iterations, def_val=5)
        self.mv.create_single_entry(root, "Nonsolid Odds", self.entry_nonsolid_odds, def_val=0.65)

        self.mv.create_single_label(root, "Number of Solid neighbors to turn...", self.label_conversion_info)

        self.mv.create_single_entry(root, "Solid?", self.entry_num_to_turn_solid, def_val=4)
        self.mv.create_single_entry(root, "NonSolid?", self.entry_num_to_turn_nonsolid, def_val=3)

    # Override implementation
    def create_section_manipulation(self, root):
        self.mv.create_button(root, "Single Iteration", self.button_iteration, on_click=self.controller.generate_iteration, state="disabled")
        return True

    # Override implementation
    def get_variables(self):
        self.variables["iterations"] = self.mv.get_entry_value_int(self.entry_iterations)
        self.variables["nonsolid_odds"] = self.mv.get_entry_value_float(self.entry_nonsolid_odds)
        self.variables["num_to_turn_solid"] = self.mv.get_entry_value_int(self.entry_num_to_turn_solid)
        self.variables["num_to_turn_nonsolid"] = self.mv.get_entry_value_int(self.entry_num_to_turn_nonsolid)

    def toggle_button_single_iteration(self, value):
        new_state = "normal" if value else "disabled"
        self.mv.toggle_widget_state(self.button_iteration, new_state)

    def get_num_to_turn_solid(self):
        return self.variables["num_to_turn_solid"]
    
    def get_num_to_turn_nonsolid(self):
        return self.variables["num_to_turn_nonsolid"]