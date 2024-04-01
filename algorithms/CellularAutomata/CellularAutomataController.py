from AlgorithmController import AlgorithmController
from algorithms.CellularAutomata.CellularAutomataModel import CellularAutomataModel

class CellularAutomataController(AlgorithmController):
    # Override implementation
    def run(self, is_seed_provided):
        super().run(is_seed_provided)
        self.view.toggle_button_single_iteration(True)

    # Override implementation
    def initialize_attributes(self, view):
        # Initialize model
        self.model = CellularAutomataModel()
        # Initialize view
        self.view = view

    def generate_iteration(self):
        self.model.generate_iteration(self.view.get_num_to_turn_solid(), self.view.get_num_to_turn_nonsolid())
        self.view.update_grid_figure()
