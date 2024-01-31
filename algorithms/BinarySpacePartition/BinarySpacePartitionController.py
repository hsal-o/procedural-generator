from AlgorithmController import AlgorithmController
from algorithms.BinarySpacePartition.BinarySpacePartitionModel import BinarySpacePartitionModel

class BinarySpacePartitionController(AlgorithmController):
    # Override implementation
    def initialize_attributes(self, view):
        # Initialize model
        self.model = BinarySpacePartitionModel()
        # Initialize view
        self.view = view