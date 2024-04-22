from tkinter import messagebox
from PIL import Image
import cv2
import threading
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import math
import statistics
from ResourceManager import ResourceManager

class GraderTabController:
    def __init__(self, view):
        self.view = view

    def run_button_on_click(self):
        def validate_selected_list(list):
            if(len(list) == 0):
                return False
            return True
        
        def print_error(error_code):
            str_error = ""
            list_missing = []

            # Missing metric(s)
            if(error_code & 1 == 1):
                list_missing.append("metric(s)")

            # Missing algorithm(s)
            if(error_code & 2 == 2):
                list_missing.append("algorithm(s)")

            if(error_code & 4 == 4):
                str_error += "- Number of trials must be atleast 2.\n"

            str_missing = ""
            for i, missing_item in enumerate(list_missing):
                if(i > 0): str_missing += ", "
                str_missing += missing_item
            str_missing = f"- The following items were not selected:\n{str_missing}"
            
            if list_missing:
                str_error += str_missing

            messagebox.showerror("Error", str_error)

        error_code = 0

        selected_metrics = [metric for metric in self.view.list_grade_metrics if self.view.get_entry_value_bool(metric.cbox) == True]
        if(validate_selected_list(selected_metrics) == False):
            error_code += 1

        selected_algorithms = [algo for algo in self.view.list_algorithms if self.view.get_entry_value_bool(algo.cbox) == True]
        if(validate_selected_list(selected_algorithms) == False):
            error_code += 2

        if(self.view.get_entry_value_int(self.view.entry_trial_count) < 2):
            error_code += 4

        if(error_code != 0):
            print_error(error_code)
            return
        
        for algorithm in selected_algorithms:
            algorithm.trial_variables = self.load_trial_variables(algorithm)

        # Continue to run without errors
        self.run_trials_threaded(selected_metrics, selected_algorithms, self.view.get_entry_value_int(self.view.entry_trial_count))

    def run_trials_threaded(self, selected_metrics, selected_algorithms, trial_count):
        # Create seperate thread
        thread = threading.Thread(target=self.run_trials, args=(selected_metrics, selected_algorithms, trial_count))
        thread.start()

    def run_trials(self, selected_metrics, selected_algorithms, trial_count):
        self.view.root.after(250, self.view.reset_progress_bar)

        total_steps = trial_count * len(selected_algorithms)
        self.view.root.after(250, self.view.set_progress_bar_maximum, total_steps)

        algorithm_data = {}

        print(f"Average metric score results for {trial_count} trials")
        for algorithm in selected_algorithms:
            # Initialize controller for algorithm
            controller = algorithm.controller_class(None)

            # Grab preset variables for trials
            trial_variables = algorithm.trial_variables

            data = {}
            data["mean_scores"] = {}
            data["median_scores"] = {}
            data["min_scores"] = {}
            data["max_scores"] = {}
            data["stdev_scores"] = {}

            mean_scores = data["mean_scores"]
            median_scores = data["median_scores"]
            min_scores = data["min_scores"]
            max_scores = data["max_scores"]
            stdev_scores = data["stdev_scores"]

            total_scores = {}

            for _ in range(trial_count):
                # Initialize and run algorithm
                controller.initialize(trial_variables)
                controller.run()

                binary_grid = controller.get_binary_grid()
                raw_grid_figure = controller.get_raw_grid_figure()
                image_path = cv2.imread(self.generate_image_path(raw_grid_figure), cv2.IMREAD_UNCHANGED)

                for metric in selected_metrics:
                    score = metric.metric_class().get_score(image_path, binary_grid)

                    # Add up mean
                    if metric.name not in mean_scores:
                        mean_scores[metric.name] = 0
                    mean_scores[metric.name] += score

                    # Store list of metric scores
                    if metric.name not in total_scores:
                        total_scores[metric.name] = []
                    total_scores[metric.name].append(score)

                    if metric.name not in median_scores:
                        median_scores[metric.name] = None

                self.view.root.after(250, self.view.update_progress_bar, 1)
  
            # Sort metric scores prior to calculations
            for metric in selected_metrics:
                total_scores[metric.name].sort()

            # Calculate mean
            for metric in mean_scores:
                mean_scores[metric] = round(mean_scores[metric] / trial_count, ResourceManager().FLOAT_PRECISION)

            # Calculate median
            for metric in median_scores:
                length = len(total_scores[metric])
                score = (total_scores[metric][ int(math.floor((length-1)/2)) ] + total_scores[metric][ int(math.ceil((length-1)/2))]) / 2
                median_scores[metric] = round(score, ResourceManager().FLOAT_PRECISION)

            # Calculate min, max, stdev
            for metric in selected_metrics:
                # Calculate min
                min_scores[metric.name] = round(min(total_scores[metric.name]), ResourceManager().FLOAT_PRECISION)
                # Calculate max
                max_scores[metric.name] = round(max(total_scores[metric.name]), ResourceManager().FLOAT_PRECISION)
                # Calcualte stdev
                stdev_scores[metric.name] = round(statistics.stdev(total_scores[metric.name]), ResourceManager().FLOAT_PRECISION)

            algorithm_data[algorithm.full_name] = data

        print()

        self.view.root.after(250, self.handle_finished_thread, selected_metrics, selected_algorithms, algorithm_data)

    def handle_finished_thread(self, selected_metrics, selected_algorithms, algorithm_data):
        messagebox.showinfo("Completed Trials", "Trials have been completed successfully!")
        self.generate_score_table(selected_metrics, selected_algorithms, algorithm_data)

    
    # def generate_score_plots(self, selected_metrics, selected_algorithms, algorithm_scores):
    #     # Clear the notebook only if it has tabs
    #     notebook = self.view.get_notebook_output()
    #     for tab_id in notebook.tabs():
    #         notebook.forget(tab_id)

    #     for metric in selected_metrics:
    #         metric_scores = [algorithm_scores[algorithm.full_name][metric.name] for algorithm in selected_algorithms]
    #         algorithm_names = [algorithm.full_name for algorithm in selected_algorithms]

    #         max_indices = [i for i, score in enumerate(metric_scores) if score == max(metric_scores)]

    #         # colors = ['skyblue' if i not in max_indices else 'orange' for i in range(len(algorithm_names))]
    #         algorithm_colors = [algorithm.color for algorithm in selected_algorithms]

    #         # Create a new figure and plot
    #         fig, ax = plt.subplots(figsize=(6, 4))
    #         bars = ax.bar(algorithm_names, metric_scores, color=algorithm_colors)
    #         ax.set_xlabel('Algorithms')
    #         ax.set_ylabel(f'Score')
    #         ax.set_title(f'{metric.name} Scores (Trial Count: {self.view.get_entry_value_int(self.view.entry_trial_count)})')
    #         ax.set_ylim(0, 1)  # Setting y-axis limits
    #         ax.grid(axis='y', linestyle='--', alpha=0.7)
    #         ax.set_xticklabels(algorithm_names, fontsize=6)

    #         for index in max_indices:
    #             bars[index].set_label('Highest Score')
    #         ax.legend()

    #         # Convert the Matplotlib figure to Tkinter compatible canvas
    #         canvas = tkagg.FigureCanvasTkAgg(fig, master=self.view.get_notebook_output())

    #         # Add canvas as a tab in the notebook, using the metric name as tab title
    #         notebook = self.view.get_notebook_output()
    #         notebook.add(canvas.get_tk_widget(), text=metric.name)


    def generate_score_table(self, selected_metrics, selected_algorithms, algorithm_data):
        # Clear the notebook only if it has tabs
        notebook = self.view.get_notebook_output()
        for tab_id in notebook.tabs():
            notebook.forget(tab_id)

        for metric in selected_metrics:
            mean_scores = [algorithm_data[algorithm.full_name]["mean_scores"][metric.name] for algorithm in selected_algorithms]
            min_scores = [algorithm_data[algorithm.full_name]["min_scores"][metric.name] for algorithm in selected_algorithms]
            max_scores = [algorithm_data[algorithm.full_name]["max_scores"][metric.name] for algorithm in selected_algorithms]
            stdev_scores = [algorithm_data[algorithm.full_name]["stdev_scores"][metric.name] for algorithm in selected_algorithms]

            algorithm_names = [algorithm.full_name for algorithm in selected_algorithms]

            # Create a new figure and plot
            fig, ax = plt.subplots(figsize=(2.5, 2))

            # Create table data
            table_data = [[name, mean, stdev, min, max] for name, mean, stdev, min, max in zip(algorithm_names, mean_scores, stdev_scores, min_scores, max_scores)]

            # Add table to the plot
            table = ax.table(cellText=table_data, colLabels=["Algorithm", "Mean", "StDev", "Min", "Max"], loc='center', cellLoc='center')
            table.auto_set_column_width(col=0)  # Auto adjust column widths

            # Customize column names appearance
            for col_idx in range(len(table_data[0])):
                cell = table.get_celld()[(0, col_idx)]
                cell.set_fontsize(8)
                cell.set_text_props(weight='bold', color='white')  # Set font weight and color
                cell.set_facecolor('grey')  # Set background color

            # Add title to the plot
            ax.set_title(f'{metric.name} Scores', fontsize=14)  # Adjust title font size and padding

            # Add text to the plot
            trial_count_text = f'Trial Count: {self.view.get_entry_value_int(self.view.entry_trial_count)}'
            ax.text(0.5, 0.95, trial_count_text, ha='center', va='center', transform=ax.transAxes, fontsize=12)

            # Hide axes
            ax.axis('off')

            # Convert the Matplotlib figure to Tkinter compatible canvas
            canvas = tkagg.FigureCanvasTkAgg(fig, master=self.view.get_notebook_output())

            canvas_widget = canvas.get_tk_widget()

            # Add canvas as a tab in the notebook, using the metric name as tab title
            notebook = self.view.get_notebook_output()
            notebook.add(canvas_widget, text=metric.name)

            

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
    