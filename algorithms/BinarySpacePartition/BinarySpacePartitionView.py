from AlgorithmView import AlgorithmView
from algorithms.BinarySpacePartition.BinarySpacePartitionController import BinarySpacePartitionController

class BinarySpacePartitionView(AlgorithmView):
    # Override implementation
    def initialize_attributes(self):
        self.controller = BinarySpacePartitionController(self)

        self.label_implement_me = self.set_widget_id("label_implement_me")

    # Override implementation
    def create_section_configuration(self, root):
        self.mv.create_single_label(root, "Implement me!", self.label_implement_me)

    # Override implementation
    def create_section_manipulation(self, root):
        return False

    # Override implementation
    def get_variables(self):
        pass