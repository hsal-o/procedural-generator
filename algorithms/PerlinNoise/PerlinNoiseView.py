from AlgorithmView import AlgorithmView
from algorithms.PerlinNoise.PerlinNoiseController import PerlinNoiseController

class PerlinNoiseView(AlgorithmView):
    # Override implementation
    def initialize_attributes(self):
        self.controller = PerlinNoiseController(self)

        # Entries
        self.entry_octave = self.set_widget_id("entry_octave")
        self.entry_lower_bound = self.set_widget_id("entry_lower_bound")
        self.entry_upper_bound = self.set_widget_id("entry_upper_bound")

        # Checkboxes
        self.cbox_show_perlin_noise = self.set_widget_id("cbox_show_perlin_noise")

    # Override implementation
    def create_section_configuration(self, root):
        # Add Entries
        self.mv.create_single_entry(root, "Octaves", self.entry_octave, def_val=6)
        self.mv.create_single_entry(root, "Lower Bound", self.entry_lower_bound, def_val=-0.12)
        self.mv.create_single_entry(root, "Upper Bound", self.entry_upper_bound, def_val=0.12)

        # Add Checboxes
        self.mv.create_single_checkbox(root, "Show Raw Perlin Noise", self.cbox_show_perlin_noise, def_val=False)

    # Override implementation
    def create_section_manipulation(self, root):
        return False

    # Override implementation
    def get_variables(self):
        # Entries
        self.variables["octave"] = self.mv.get_entry_value_int(self.entry_octave)
        self.variables["lower_bound"] = self.mv.get_entry_value_float(self.entry_lower_bound)
        self.variables["upper_bound"] = self.mv.get_entry_value_float(self.entry_upper_bound)

        # Checboxes
        self.variables["show_perlin_noise"] = self.mv.get_entry_value_bool(self.cbox_show_perlin_noise)