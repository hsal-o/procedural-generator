import tkinter as tk
from tkinter import ttk
from tabs.GraderTabView import GraderTabView
from tabs.GenerationTabView import GenerationTabView

class MainView:
    def __init__(self):
        self.create_window() # Create main window
        self.root.mainloop() # Start the Tkinter event loop

    ################################################################################
    # Main Window
    ################################################################################
    def create_window(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("CaveGen Labs")

        # Create notebook tab style
        style = ttk.Style(self.root)
        # style.configure('TopTab.TNotebook', tabposition='nw', background=self.colors["gray-500"])
        style.configure('TopTab.TNotebook', tabposition='nw')
        # Create container
        container = ttk.Notebook(self.root, style="TopTab.TNotebook")
        container.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        GenerationTabView(self.root).create(container)
        GraderTabView(self.root).create(container)
