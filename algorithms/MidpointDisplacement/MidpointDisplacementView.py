import tkinter as tk
from AlgorithmView import AlgorithmView
from algorithms.MidpointDisplacement.MidpointDisplacementController import MidpointDisplacementController


class MidpointDisplacementView(AlgorithmView):

    class Preset:
        def __init__(self, algorithm, variables, state="disabled"):
            self.algorithm = algorithm
            self.variables = variables
            self.state = state
        
        def apply(self):
            print("Ran Preset.apply()!")
            self.algorithm.preset_variables(self.variables, self.state)

    # Override implementation
    def initialize_attributes(self):
        self.controller = MidpointDisplacementController(self)

        # Entries
        self.entry_magnitude        = self.set_widget_id("entry_magnitude")
        self.entry_iterations       = self.set_widget_id("entry_iterations")
        self.entry_stroke_thickness = self.set_widget_id("entry_stroke_thickness")
        self.entry_start_x          = self.set_widget_id("entry_start_x")
        self.entry_start_y          = self.set_widget_id("entry_start_y")
        self.entry_end_x            = self.set_widget_id("entry_end_x")
        self.entry_end_y            = self.set_widget_id("entry_end_y")

        # Checkboxes
        self.cbox_randomize_stroke_thickness = self.set_widget_id("cbox_randomize_stroke_thickness")

    ################################################################################
    # Preset Creation
    ################################################################################

    def preset_variables(self, variables, state):
        self.mv.set_entry_value(self.entry_magnitude, variables["magnitude"], state=state)
        self.mv.set_entry_value(self.entry_iterations, variables["iterations"], state=state)
        self.mv.set_entry_value(self.entry_stroke_thickness, variables["stroke_thickness"], state=state)
        self.mv.set_entry_value(self.entry_start_x, variables["x1"], state=state)
        self.mv.set_entry_value(self.entry_start_y, variables["y1"], state=state)
        self.mv.set_entry_value(self.entry_end_x, variables["x2"], state=state)
        self.mv.set_entry_value(self.entry_end_y, variables["y2"], state=state)

    ################################################################################
    # Section Creation
    ################################################################################
    # Override implementation
    def create_section_configuration(self, root):
        # Add single Entries
        self.mv.create_single_entry(root, "Magnitude",        self.entry_magnitude) # 16
        self.mv.create_single_entry(root, "Iterations",       self.entry_iterations) # 5
        self.mv.create_single_entry(root, "Stroke Thickness", self.entry_stroke_thickness) # 3

        # Add double entries
        self.mv.create_dual_entry(root, "Start (x, y)", self.entry_start_x, self.entry_start_y) 
        self.mv.create_dual_entry(root, "End (x, y)",   self.entry_end_x, self.entry_end_y)

        # Add Checkboxes
        self.mv.create_single_checkbox(root, "Randomize Line Thickess", self.cbox_randomize_stroke_thickness, def_val=True)



    # Override parent
    def create_section_presets(self, root):
        self.radio_button_var = tk.IntVar()

        # Create custom Preset
        custom_variables = {}
        custom_variables["magnitude"] = None
        custom_variables["iterations"] = None
        custom_variables["stroke_thickness"] = None
        custom_variables["x1"] = None
        custom_variables["y1"] = None
        custom_variables["x2"] = None
        custom_variables["y2"] = None
        self.preset_custom = self.Preset(self, custom_variables, state="normal")
        # Create Button
        self.rb_custom = self.set_widget_id("rb_custom")
        self.mv.create_radio_button(root, "Custom", self.rb_custom, self.radio_button_var, 1, command=self.preset_custom.apply)

        # Create default Preset
        default_variables = {}
        default_variables["magnitude"] = 6
        default_variables["iterations"] = 5
        default_variables["stroke_thickness"] = 3
        default_variables["x1"] = 0
        default_variables["y1"] = 0
        default_variables["x2"] = self.mv.get_entry_width()-1
        default_variables["y2"] = self.mv.get_entry_height()-1
        self.preset_default = self.Preset(self, default_variables)
        # Create Button
        self.rb_default = self.set_widget_id("rb_default")
        self.mv.create_radio_button(root, "Default", self.rb_default, self.radio_button_var, 2, command=self.preset_default.apply)

        # Apply default preset
        self.radio_button_var.set(2)
        self.preset_default.apply()

    ################################################################################
    # Getters/Setters
    ################################################################################
    # Override implementation
    def get_variables(self):
        self.variables["magnitude"]              = self.mv.get_entry_value_int(self.entry_magnitude)
        self.variables["iterations"]             = self.mv.get_entry_value_int(self.entry_iterations)
        self.variables["stroke_thickness"]       = self.mv.get_entry_value_int(self.entry_stroke_thickness)
        self.variables["do_random_thickness"]    = self.mv.get_entry_value_bool(self.cbox_randomize_stroke_thickness)

        self.variables["x1"] = self.mv.get_entry_value_int(self.entry_start_x)
        self.variables["y1"] = self.mv.get_entry_value_int(self.entry_start_y)
        self.variables["x2"] = self.mv.get_entry_value_int(self.entry_end_x)
        self.variables["y2"] = self.mv.get_entry_value_int(self.entry_end_y)
