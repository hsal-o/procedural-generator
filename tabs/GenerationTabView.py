import tkinter as tk

class GenerationTabView:
    def __init__(self, main_view):
        self.mv = main_view

    def create_tab(self, root):
        # Create container 
        container = tk.Frame(root)
        container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create input and output frames
        self.create_input_frame(container)
        self.create_output_frame(container)

        # Add container to root
        root.add(container, text="Generation")