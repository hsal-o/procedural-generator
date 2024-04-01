import tkinter as tk
from tabs.TabView import TabView

class GradeMetric:
    def __init__(self, cbox, name):
        self.cbox = cbox
        self.name = name

class GraderTabView(TabView):
    def __init__(self, root):
        super(GraderTabView, self).__init__(root)

        # Widget variables
        self.cbox_metric_roughness = "cbox_metric_roughness"
        self.cbox_metric_openness = "cbox_metric_openness"
        self.cbox_metric_narrowness = "cbox_metric_narrowness"
        self.cbox_metric_connectivity = "cbox_metric_connectivity"
        self.cbox_metric_branching = "cbox_metric_branching"
        self.cbox_metric_all = "cbox_metric_all"
        self.cbox_algorithm_all = "cbox_algorithm_all"

    # Helper method
    def set_all_cbox_in_list(self, list, value):
        if(value == False):
            return
        for item in list:
            self.set_cbox(item.cbox, True)

    # Method to create overall tab view
    def create_tab(self, root):
        # Create container
        container = tk.Frame(root)
        container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create sections
        self.create_metrics_section(container)
        self.create_algorithms_section(container)
        self.create_grade_output_section(container)

        # Add container to root
        root.add(container, text="Grader")

    # Method to create metrics section
    def create_metrics_section(self, root):
        # Create container
        container = tk.Frame(root, background="#FBFCFC")
        container.pack(side=tk.LEFT, fill=tk.Y)

        # Create label header
        label_header = tk.Label(container, text=f"Metrics", font=("Helvetica", 12, "bold"), background=container.cget("bg"))
        label_header.pack()

        self.list_grade_metrics = []
        self.list_grade_metrics.append(GradeMetric(self.cbox_metric_roughness, "Roughness"))
        self.list_grade_metrics.append(GradeMetric(self.cbox_metric_openness, "Openness"))
        self.list_grade_metrics.append(GradeMetric(self.cbox_metric_narrowness, "Narrowness"))
        self.list_grade_metrics.append(GradeMetric(self.cbox_metric_connectivity, "Connectivity"))
        self.list_grade_metrics.append(GradeMetric(self.cbox_metric_branching, "Branching"))

        # Create metric checkboxes
        for metric in self.list_grade_metrics:
            self.create_single_checkbox(container, metric.name, metric.cbox, def_val=False, command=lambda: self.set_cbox(self.cbox_metric_all, False)) 
        # Create select all checkbox
        self.create_single_checkbox(container, "SELECT ALL", self.cbox_metric_all, def_val=False, command=lambda: self.set_all_cbox_in_list(self.list_grade_metrics, self.get_entry_value_bool(self.cbox_metric_all)))
    
    # Method to create algorithms section
    def create_algorithms_section(self, root):
        # Create container
        container = tk.Frame(root)
        container.pack(side=tk.LEFT, fill=tk.Y)

        # Create label header
        label_header = tk.Label(container, text=f"Algorithms", font=("Helvetica", 12, "bold"), background=container.cget("bg"))
        label_header.pack()

        # Create algorithm checkboxes
        for tab in self.get_list_algorithms():
            self.create_single_checkbox(container, tab.full_name, tab.cbox, def_val=False, command=lambda: self.set_cbox(self.cbox_algorithm_all, False))
        # Create select all checkbox
        self.create_single_checkbox(container, "SELECT ALL", self.cbox_algorithm_all, def_val=False, command=lambda: self.set_all_cbox_in_list(self.get_list_algorithms(), self.get_entry_value_bool(self.cbox_algorithm_all)))    

    # Method to create output section
    def create_grade_output_section(self, root):
        # Create container
        container = tk.Frame(root, background="white")
        container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create label header
        label_header = tk.Label(container, text=f"Output", font=("Helvetica", 12, "bold"), background=container.cget("bg"))
        label_header.pack()