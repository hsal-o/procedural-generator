import importlib
import os
import copy

class Algorithm:
    def __init__(self, full_name, nickname, color, view_class, controller_class, view, order):
        self.full_name = full_name
        self.nickname = nickname
        self.color = color
        self.view_class = view_class    # AlgorithmView class for specific algorithm
        self.controller_class = controller_class
        self.view = view                # View this algorithm will be used in
        self.order = order
        self.cbox = "cbox_" + self.nickname

    def set_view(self, view):
        self.view = self.view_class(view, self.full_name)

class GradeMetric:
    def __init__(self, name, metric_class, order):
        self.name = name
        self.metric_class = metric_class
        self.order = order
        self.cbox = "cbox_" + self.name


class ResourceManager:
    _instance = None
    
    def __new__(self):
        if self._instance is None:
            self._instance = super().__new__(self)
            self._instance.load_algorithms()  # Load only once
            self._instance.load_grade_metrics() # Load only once
        return self._instance
    
    def __init__(self):
        pass
    
    def load_algorithms(self):
        self.list_algorithms = []

        # Get a list of algorithm folders
        algorithm_folder_name = "algorithms"
        algorithm_folders = [f for f in os.listdir(algorithm_folder_name) if os.path.isdir(os.path.join(algorithm_folder_name, f)) and not f.startswith("__")]
        
        for algorithm in algorithm_folders:
            # Dynamically import components
            algorithm_package = importlib.import_module(f'algorithms.{algorithm}')

            # Grab algorithm names from __init__.py
            algorithm_full_name = getattr(algorithm_package, "algorithm_full_name", "Unknown")
            algorithm_nickname = getattr(algorithm_package, "algorithm_nickname", "Unknown")
            algorithm_color = getattr(algorithm_package, "algorithm_color", "Unknown")
            algorithm_order = getattr(algorithm_package, "algorithm_order", "Unknown")

            # Import specific components
            view_module = importlib.import_module(f"algorithms.{algorithm}.{algorithm}View")
            controller_module = importlib.import_module(f"algorithms.{algorithm}.{algorithm}Controller")

            # Access algorithm classes
            algorithm_view_class = getattr(view_module, f"{algorithm}View", None)
            algorithm_controller_class = getattr(controller_module, f"{algorithm}Controller", None)

            algorithm = Algorithm(full_name=algorithm_full_name, 
                                  nickname=algorithm_nickname, 
                                  view_class=algorithm_view_class,
                                  controller_class=algorithm_controller_class,
                                  view=None, 
                                  color=algorithm_color, 
                                  order=algorithm_order)
            
            # Add algorithm to list
            self.list_algorithms.append(algorithm)

        # Order list_algorithms accordingly
        self.list_algorithms = sorted(self.list_algorithms, key=lambda x: x.order)

    def load_grade_metrics(self):
        self.list_grade_metrics = []

        # Get a list of grade metric folders
        metric_folder_name = "graders"
        metric_folders = [f for f in os.listdir(metric_folder_name) if os.path.isdir(os.path.join(metric_folder_name, f)) and not f.startswith("__")]

        for metric in metric_folders:
            # Dynamically import components
            metric_package = importlib.import_module(f"{metric_folder_name}.{metric}")

            # Grab variables from __init__.py
            metric_name = getattr(metric_package, "metric_name", "Unknown")
            metric_order = getattr(metric_package, "metric_order", "Unknown")

            # Importy specific components
            module = importlib.import_module(f"{metric_folder_name}.{metric}.{metric}")

            # Access metric classes
            metric_class = getattr(module, f"{metric}", "None")

            metric = GradeMetric(name=metric_name,
                                 metric_class=metric_class,
                                 order=metric_order)
            
            # Add metric to list
            self.list_grade_metrics.append(metric)
        
        # Order list_grade_metrics accordingly
        self.list_grade_metrics = sorted(self.list_grade_metrics, key=lambda x: x.order)

    def get_list_algorithms(self):
        return self.list_algorithms

    def get_list_grade_metrics(self):
        return self.list_grade_metrics
    
    # Returns a copy of list_algorithms that is adapted to fit the provided view
    def get_fitted_algorithm_list(self, view):
        new_list_algorithms = copy.deepcopy(self.list_algorithms)

        for algorithm in new_list_algorithms:
            algorithm.set_view(view)

        return new_list_algorithms