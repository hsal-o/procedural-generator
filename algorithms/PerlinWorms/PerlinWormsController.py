from AlgorithmController import AlgorithmController
from algorithms.PerlinWorms.PerlinWormsModel import PerlinWormsModel

class PerlinWormsController(AlgorithmController):
    # Override implementation
    def initialize_attributes(self, view):
        # Initialize model
        self.model = PerlinWormsModel()
        # Initialize view
        self.view = view

    def get_binary_grid(self):
        return self.model.get_binary_grid()