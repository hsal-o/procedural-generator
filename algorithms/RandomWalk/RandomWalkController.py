from AlgorithmController import AlgorithmController
from algorithms.RandomWalk.RandomWalkModel import RandomWalkModel

class RandomWalkController(AlgorithmController):
    # Override implementation
    def initialize_attributes(self, view):
        # Initialize model
        self.model = RandomWalkModel()
        # Initialize view
        self.view = view