import os
import tkinter as tk
from tkinter import ttk
from tabs.TabView import TabView
from PIL import ImageGrab 
from datetime import datetime
from tabs.GraderTabController import GraderTabController

class GraderTabView(TabView):
    def __init__(self, root):
        super(GraderTabView, self).__init__(root)

        # Widget variables
        self.cbox_metric_all = "cbox_metric_all"
        self.cbox_algorithm_all = "cbox_algorithm_all"

        self.entry_trial_count = "entry_trial_count"
        self.button_run = "button_run"
        self.button_screenshot_screen = "button_screenshot_screen"
        self.button_screenshot_graph = "button_screenshot_graph"

        self.progress_bar = "progress_bar"

        self.frame_output = "frame_output"
        self.notebook_output = "notebook_output"

        self.controller = GraderTabController(self)

    # Helper method
    def set_all_cbox_in_list(self, list, value):
        if(value == False):
            return
        for item in list:
            self.set_cbox(item.cbox, True)

    # Method to create overall tab view
    def create(self, root):
        # Create container
        container = tk.Frame(root)
        container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create sections
        self.create_metrics_section(container)
        self.create_algorithms_section(container)
        self.create_generation_configuration_section(container)
        self.create_grade_output_section(container)

        # Add container to root
        root.add(container, text="Grader")

    # Method to create metrics section
    def create_metrics_section(self, root):
        # Create container
        container = tk.LabelFrame(root, text="Metrics", background=root.cget("bg"))
        container.pack(side=tk.LEFT, fill=tk.Y)

        # Create metric checkboxes
        for metric in self.list_grade_metrics:
            self.create_single_checkbox(container, metric.name, metric.cbox, def_val=False, command=lambda: self.set_cbox(self.cbox_metric_all, False)) 
        # Create select all checkbox
        self.create_single_checkbox(container, "SELECT ALL", self.cbox_metric_all, def_val=False, command=lambda: self.set_all_cbox_in_list(self.list_grade_metrics, self.get_entry_value_bool(self.cbox_metric_all)))
    
    # Method to create algorithms section
    def create_algorithms_section(self, root):
        # Create container
        container = tk.Frame(root)
        container = tk.LabelFrame(root, text="Algorithms", background=root.cget("bg"))
        container.pack(side=tk.LEFT, fill=tk.Y)

        # Create algorithm checkboxes
        for algorithm in self.get_list_algorithms():
            self.create_single_checkbox(container, algorithm.full_name, algorithm.cbox, def_val=False, command=lambda: self.set_cbox(self.cbox_algorithm_all, False))
        # Create select all checkbox
        self.create_single_checkbox(container, "SELECT ALL", self.cbox_algorithm_all, def_val=False, command=lambda: self.set_all_cbox_in_list(self.get_list_algorithms(), self.get_entry_value_bool(self.cbox_algorithm_all)))    

    def create_generation_configuration_section(self, root):
        # Create container
        container = tk.LabelFrame(root, text="Trials", background=root.cget("bg"))
        container.pack(side=tk.LEFT, fill=tk.Y)

        # Create entry
        self.create_single_entry(container, "Trial count", self.entry_trial_count, def_val=2)

        button_container = tk.Frame(container, background=root.cget("bg"))
        button_container.pack(fill=tk.X, padx=self.padding["small"])

        # Create Button
        self.create_button(button_container, "RUN", self.button_run, on_click=self.controller.run_button_on_click, height=2, bg="#D6DBDF")
        self.widget_map[self.button_run].pack(pady=self.padding["regular"])

        # Create Progress bar
        self.widget_map[self.progress_bar] = ttk.Progressbar(container)
        self.widget_map[self.progress_bar].pack(padx=self.padding["small"], pady=(self.padding["small"], self.padding["regular"]), fill=tk.X)

        #######
        screenshot_container = tk.LabelFrame(container, text="Screenshot", background=container.cget("bg"))
        screenshot_container.pack(fill=tk.X, padx=self.padding["regular"], pady=(0, self.padding["regular"]))


        self.create_dual_buttons(screenshot_container, 
                                 label_1="Screen", 
                                 button_1=self.button_screenshot_screen, 
                                 on_click_1=self.button_screenshot_screen_on_click, 
                                 label_2="Graph", 
                                 button_2=self.button_screenshot_graph, 
                                 on_click_2=self.button_screenshot_graph_on_click)

    # Method to create output section
    def create_grade_output_section(self, root):
        # Create container
        self.widget_map[self.frame_output] = tk.LabelFrame(root, text="Output", background=root.cget("bg"))
        container = self.widget_map[self.frame_output]
        container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create notebook
        self.widget_map[self.notebook_output] = ttk.Notebook(container)
        notebook = self.widget_map[self.notebook_output]
        notebook.pack(fill=tk.BOTH, expand=True)

    def update_progress_bar(self, step):
        self.widget_map[self.progress_bar].step(step)

    def reset_progress_bar(self):
        self.widget_map[self.progress_bar].configure(value=0)
    
    def set_progress_bar_maximum(self, max):
        self.widget_map[self.progress_bar].configure(maximum=max)

    def get_notebook_output(self):
        return self.widget_map[self.notebook_output]
    
    def button_screenshot_screen_on_click(self):
        # Get the Tkinter window dimensions
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Capture the screenshot using ImageGrab
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        # # Save the screenshot to a file
        self.show_screenshot_popup(screenshot, "GraderTab")
    
    def button_screenshot_graph_on_click(self):
        # Get the currently selected notebook tab
        notebook = self.get_notebook_output()
        selected_tab_index = notebook.index("current")

        # Get the canvas widget associated with the selected tab
        canvas_widget = notebook.winfo_children()[selected_tab_index]

        # Get dimensions of canvas
        x = canvas_widget.winfo_rootx()
        y = canvas_widget.winfo_rooty()
        width = canvas_widget.winfo_width()
        height = canvas_widget.winfo_height()

        # Capture screenshot using ImageGrab
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        # Parent folder
        parent_folder = "screenshots"

        # Define specific screenshots folder
        screenshots_folder = os.path.join(parent_folder, "metric-graph-screenshots")
        os.makedirs(screenshots_folder, exist_ok=True)

        file_name = f"screenshot_tab_{selected_tab_index}.png"

        # Get date and time
        current_datetime = datetime.now()
        time_stamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

        # Create file name
        file_name = f"{screenshots_folder}/{time_stamp}_{selected_tab_index}_Grid.png"

        # Save the screenshot as file
        screenshot.save(file_name)
        screenshot.show()
