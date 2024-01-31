from AlgorithmController import AlgorithmController
from algorithms.PerlinNoise.PerlinNoiseModel import PerlinNoiseModel

class PerlinNoiseController(AlgorithmController):
    # Override implementation
    def initialize_attributes(self, view):
        # Initialize model
        self.model = PerlinNoiseModel()
        # Initialize view
        self.view = view