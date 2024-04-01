import importlib
import os
import copy

class Algorithm:
    def __init__(self, full_name, nickname, color, view_class, view, order):
        self.full_name = full_name
        self.nickname = nickname
        self.color = color
        self.view_class = view_class    # AlgorithmView class for specific algorithm
        self.view = view                # View this algorithm will be used in
        self.order = order
        self.cbox = self.nickname

    def set_view(self, view):
        self.view = self.view_class(view, self.full_name)

class ResourceManager:
    _instance = None
    
    def __new__(self):
        if self._instance is None:
            self._instance = super().__new__(self)
            self._instance.load_algorithms()  # Load only once
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

            # Access algorithmView class
            algorithm_view_class = getattr(view_module, f'{algorithm}View', None)

            # Create algorithm data object
            # algorithm = Algorithm(full_name=algorithm_full_name, 
            #                       nickname=algorithm_nickname, 
            #                       view=view_class(self, algorithm_full_name), 
            #                       color=algorithm_color, 
            #                       order=algorithm_order)

            algorithm = Algorithm(full_name=algorithm_full_name, 
                                  nickname=algorithm_nickname, 
                                  view_class=algorithm_view_class,
                                  view=None, 
                                  color=algorithm_color, 
                                  order=algorithm_order)
            
            # Add algorithm to list
            self.list_algorithms.append(algorithm)

        # Order list_algorithms accordingly
        self.list_algorithms = sorted(self.list_algorithms, key=lambda x: x.order)

    def get_algorithm_list(self):
        return self.list_algorithms
    
    # Returns a copy of list_algorithms that is adapted to fit the provided view
    def get_fitted_algorithm_list(self, view):
        new_list_algorithms = copy.deepcopy(self.list_algorithms)

        for algorithm in new_list_algorithms:
            algorithm.set_view(view)

        return new_list_algorithms