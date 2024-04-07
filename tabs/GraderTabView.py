import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tabs.TabView import TabView
from PIL import Image
import cv2
import importlib
import os

# class GradeMetric:
#     def __init__(self, cbox, name):
#         self.cbox = cbox
#         self.name = name

class GraderTabView(TabView):
    def __init__(self, root):
        super(GraderTabView, self).__init__(root)

        # Widget variables
        self.cbox_metric_all = "cbox_metric_all"
        self.cbox_algorithm_all = "cbox_algorithm_all"

        self.entry_trial_count = "entry_trial_count"
        self.button_run = "button_run"

        self.progress_bar = "progress_bar"

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
        self.create_single_entry(container, "Trial count", self.entry_trial_count, def_val=1)

        button_container = tk.Frame(container, background=root.cget("bg"))
        button_container.pack(fill=tk.X, padx=self.padding["small"])

        # Create Button
        self.create_button(button_container, "RUN", self.button_run, on_click=self.run_button_on_click, height=2, bg="#D6DBDF")

        # # Create Progress bar
        # self.widget_map[self.progress_bar]  = ttk.Progressbar(container)
        # self.widget_map[self.progress_bar].pack(padx=self.padding["small"], fill=tk.X)


    # Method to create output section
    def create_grade_output_section(self, root):
        # Create container
        container = tk.Frame(root, background="white")
        container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create label header
        label_header = tk.Label(container, text=f"Output", font=("Helvetica", 12, "bold"), background=container.cget("bg"))
        label_header.pack()


    def run_button_on_click(self):

        def validate_selected_list(list):
            if(len(list) == 0):
                return False
            # for item in list:
            #     print(f"{item.cbox} was selected!")
            return True
        
        def print_error(error_code):
            list_missing = []

            # Missing metric(s)
            if(error_code & 1 == 1):
                list_missing.append("metric(s)")

            # Missing algorithm(s)
            if(error_code & 2 == 2):
                list_missing.append("algorithm(s)")

            str_missing = ""
            for i, missing_item in enumerate(list_missing):
                if(i > 0): str_missing += ", "
                str_missing += missing_item

            messagebox.showerror("Missing Selection(s)", f"Error: The following items were not selected:\n{str_missing}")

        error_code = 0

        selected_metrics = [metric for metric in self.list_grade_metrics if self.get_entry_value_bool(metric.cbox) == True]
        if(validate_selected_list(selected_metrics) == False):
            error_code += 1

        selected_algorithms = [algo for algo in self.list_algorithms if self.get_entry_value_bool(algo.cbox) == True]
        if(validate_selected_list(selected_algorithms) == False):
            error_code += 2

        if(error_code != 0):
            print_error(error_code)
            return

        # Continue to run without errors
        self.run_trials(selected_metrics, selected_algorithms, self.get_entry_value_int(self.entry_trial_count))

    def run_trials(self, selected_metrics, selected_algorithms, trial_count):
        # self.widget_map[self.progress_bar].configure(value = 0)
        # self.widget_map[self.progress_bar].configure(maximum = trial_count*len(selected_algorithms))

        print(f"Average metric score results for {trial_count} trials")
        for algorithm in selected_algorithms:
            # Initialize controller for algorithm
            controller = algorithm.controller_class(None)

            # Grab preset variables for trials
            trial_variables = self.load_trial_variables(algorithm)

            metric_scores = {}

            for _ in range(trial_count):
                # Initialize and run algorithm
                controller.initialize(trial_variables)
                controller.run()

                binary_grid = controller.get_binary_grid()
                raw_grid_figure = controller.get_raw_grid_figure()
                image_path = cv2.imread(self.generate_image_path(raw_grid_figure), cv2.IMREAD_UNCHANGED)


                for metric in selected_metrics:
                    score = metric.metric_class().get_score(image_path, binary_grid)

                    if metric.name not in metric_scores:
                        metric_scores[metric.name] = 0

                    metric_scores[metric.name] += round(score, 6)

                # self.widget_map[self.progress_bar].step(1)

            # print(f"~~SEED: {controller.get_seed()}")
            for metric in metric_scores:
                metric_scores[metric] = round(metric_scores[metric] / trial_count, 3)
            print(f"[{algorithm.full_name}] //")
            print(f"{metric_scores}")


        print()



    # Helper Methods
    def load_trial_variables(self, algorithm):
        preset_name = "trial.conf"
        file = open(f"algorithms/{algorithm.full_name.replace(' ', '')}/presets/{preset_name}", "r")

        trial_variables = {}
        for line in file:
            data = line.strip().split(',')

            type = data[0].strip()
            variable = data[1].strip()
            match type:
                case "INT":
                    value = int(data[2].strip())
                case "FLOAT":
                    value = float(data[2].strip())
                case "BOOL":
                    value = bool(int(data[2].strip()))

            trial_variables[variable] = value

        return trial_variables
    
    def generate_image_path(self, raw_grid_figure):
        # CHECK IF tmp FOLDER EXISTS
        image_path = "tmp/tmp.png" # Assumes tmp folder exists

        grid_height = raw_grid_figure.shape[0]  
        grid_width = raw_grid_figure[0].shape[0]
        image = Image.fromarray(raw_grid_figure)

        multiplier = 20
        desired_size = (grid_width * multiplier, grid_height * multiplier)

        # Resize the image to the desired size while maintaining the aspect ratio
        image = image.resize(desired_size, Image.Resampling.NEAREST) 

        image.save(image_path)

        return image_path
    
