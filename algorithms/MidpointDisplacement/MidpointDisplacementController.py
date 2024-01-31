from AlgorithmController import AlgorithmController
from algorithms.MidpointDisplacement.MidpointDisplacementModel import MidpointDisplacementModel

class MidpointDisplacementController(AlgorithmController):
    # Override implementation
    def initialize_attributes(self, view):
        # Initialize model
        self.model = MidpointDisplacementModel()
        # Initialize view
        self.view = view