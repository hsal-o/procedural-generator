import importlib
import os
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2
from PIL import Image, ImageGrab, ImageTk
from datetime import datetime
from tabs.TabView import TabView
from ResourceManager import ResourceManager

import sys
sys.path.append("..")

from graders.RoughnessGrader import RoughnessGrader

class GenerationTabView(TabView):
    def __init__(self, root):
        super(GenerationTabView, self).__init__(root)

        self.canvas = None

        self.colors = {
            "gray-500": "#D5D8DC",
        }

        # Frames
        self.input_frame = None
        self.output_frame = None

        # Entries
        self.entry_width            = "entry_width"
        self.entry_height           = "entry_height"
        self.entry_seed             = "entry_seed"

        # Buttons
        self.button_export = "button_export"
        self.button_import = "button_import"
        self.button_flip_x = "button_flip_x"
        self.button_flip_y = "button_flip_y"
        self.button_generate = "button_generate"
        self.button_grade = "button_grade"
        self.button_screenshot_screen = "button_screenshot_screen"
        self.button_screenshot_grid = "button_screenshot_grid"

        self.list_algorithms = ResourceManager().get_fitted_algorithm_list(self)

        # Set algorithm view to first tab
        self.algorithm_view = self.list_algorithms[0]


    def get_entry_seed(self):
        return self.get_entry_value_int(self.entry_seed)

    def set_entry_seed(self, seed):
        previously_disabled = False
        if(str(self.widget_map[self.entry_seed].cget("state")).strip() == "readonly"):
            previously_disabled = True
            self.widget_map[self.entry_seed].config(state="normal")

        self.widget_map[self.entry_seed].delete(0, tk.END) 
        self.widget_map[self.entry_seed].insert(0, seed) 

        if(previously_disabled):
            self.widget_map[self.entry_seed].config(state="readonly")

    def create(self, root):
        # Create container 
        container = tk.Frame(root)
        container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create input and output frames
        self.create_input_frame(container)
        self.create_output_frame(container)

        # Add container to root
        root.add(container, text="Generation")

    # Seed Entry
    def create_seed_entry(self, root):
        # Inner function
        def toggle_entry_seed_state():
            if self.get_entry_value_bool(self.cbox_using_seed) == True:
                self.toggle_widget_state(self.entry_seed, "normal")
            else:
                self.toggle_widget_state(self.entry_seed, "readonly")

        # Create container
        container = tk.Frame(root, background=root.cget("bg"))
        container.pack(padx=(0,self.padding["regular"]),pady=self.padding["small"])

        # Instantiate control variable
        self.cbox_using_seed = "cbox_use_seed"
        self.widget_map[self.cbox_using_seed] = tk.BooleanVar()
        self.widget_map[self.cbox_using_seed].set(False)

        # Create checkbox and assign it the control variable
        checkbox = tk.Checkbutton(container, text=f"Set Seed", variable=self.widget_map[self.cbox_using_seed], command=toggle_entry_seed_state)
        checkbox.pack(side=tk.LEFT)            

        # Add entry to container
        self.widget_map[self.entry_seed] = ttk.Entry(container)
        self.widget_map[self.entry_seed].pack(side=tk.RIGHT)
        self.widget_map[self.entry_seed].config(state="readonly")

    ################################################################################
    # Overall Input Frame creation
    ################################################################################
    def create_input_frame(self, root):
        # Create container for inputs
        container = tk.Frame(root)
        container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create generic + specific frames within container
        self.create_generic_frame(container)
        self.create_specific_frame(container)

    # ------------------------------------------------------------------------------
    # Generic Input Frame Creation
    # ------------------------------------------------------------------------------
    def create_generic_frame(self, root):
        # Create container
        container = tk.Frame(root)
        container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create sections within container
        self.create_section_grid_configuration(container)
        self.create_section_grid_generation(container)
        self.create_section_screenshot(container)
        self.create_section_grid_manipulation(container)

    # Configuration section creation    
    def create_section_grid_configuration(self, root):
        # Create container
        container = tk.LabelFrame(root, text="Grid Configuration", background=root.cget("bg"))
        container.pack(fill=tk.X, padx=self.padding["regular"], pady=self.padding["regular"])

        # Add Widgets
        self.create_single_entry(container, "Width", self.entry_width, def_val=32)
        self.create_single_entry(container, "Height", self.entry_height, def_val=32)
        self.create_seed_entry(container)

    # Generation section creation  
    def create_section_grid_generation(self, root):
        # Create container
        container = tk.Frame(root, background=root.cget("bg"))
        container.pack(fill=tk.X, padx=self.padding["small"])

        # Add Widgets
        self.create_button(container, "GENERATE", self.button_generate, on_click=self.generate_button_on_click, height=2, bg="#D6DBDF")
        self.create_button(container, "GRADE", self.button_grade, on_click=self.grade_button_on_click, height=2, bg="#F8F9F9")
        
    def create_section_screenshot(self, root):
        container = tk.LabelFrame(root, text="Screenshot", background=root.cget("bg"))
        container.pack(fill=tk.X, padx=self.padding["regular"], pady=(0, self.padding["regular"]))

        self.create_dual_buttons(container, 
                                 label_1="Screen", 
                                 button_1=self.button_screenshot_screen, 
                                 on_click_1=self.button_screenshot_screen_on_click, 
                                 label_2="Grid", 
                                 button_2=self.button_screenshot_grid, 
                                 on_click_2=self.button_screenshot_grid_on_click)

    # Manipulation section creation  
    def create_section_grid_manipulation(self, root):
        # Create container
        self.section_grid_manipulation = "section_grid_manipulation"
        self.widget_map[self.section_grid_manipulation] = tk.LabelFrame(root, text="Grid Manipulation", background=root.cget("bg"))
        self.widget_map[self.section_grid_manipulation].pack(fill=tk.X, padx=self.padding["regular"], pady=(0, self.padding["regular"]))

        # Add Widgets
        self.create_dual_buttons(self.widget_map[self.section_grid_manipulation], label_1="Export Grid", button_1=self.button_export, on_click_1=self.button_export_on_click, 
                                            label_2="Import Grid", button_2=self.button_import, on_click_2=self.button_import_on_click)
        self.create_dual_buttons(self.widget_map[self.section_grid_manipulation], label_1="Flip X Axis", button_1=self.button_flip_x, on_click_1=self.button_flip_x_on_click, 
                                            label_2="Flip Y Axis", button_2=self.button_flip_y, on_click_2=self.button_flip_y_on_click)
        
        # Disable all buttons by default, (Grid hasn't been generated)
        self.toggle_section_grid_manipulation(False)

    # ------------------------------------------------------------------------------
    # Specific Input Frame Creation
    # ------------------------------------------------------------------------------
    def create_specific_frame(self, root):
        # Function to switch view based on selected tab
        def switch_view(event):
            selected_index = container.index(container.select())
            self.algorithm_view = self.list_algorithms[selected_index]
            self.widget_map[self.button_generate].config(command=self.generate_button_on_click)

        # Create notebook tab style
        style = ttk.Style(root)
        style.configure('LeftTab.TNotebook', tabposition='wn', background=self.colors["gray-500"])

        # Create container
        container = ttk.Notebook(root, style='LeftTab.TNotebook')
        container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        container.bind("<<NotebookTabChanged>>", switch_view)

        # Create algorithm tabs dynamically
        for algorithm in self.list_algorithms:
            self.create_tab(container, algorithm)

    def create_tab(self, root, algorithm):
        # Create container
        container = tk.Frame(root, bg=algorithm.color)
        container.pack(side=tk.LEFT)

        # Create label header
        label_header = tk.Label(container, text=f"{algorithm.full_name}", font=("Helvetica", 12, "bold"), background=container.cget("bg"))
        label_header.pack()

        # Create section for specific algorithm
        self.create_section_algorithm_configuration(algorithm, container)
        self.create_section_algorithm_manipulation(algorithm, container)
        self.create_section_algorithm_presets(algorithm, container)

        # Add container to root
        root.add(container, text="{:^20}".format(algorithm.nickname))

    def create_section_algorithm_configuration(self, algorithm, root):
        # Create container
        container = tk.LabelFrame(root, text="Algorithm Configuration", background=root.cget("bg"))
        container.pack(fill=tk.X, padx=10, pady=(0, self.padding["regular"]))

        # Create algorithm section and add to container
        algorithm.view.create_section_configuration(container)

    def create_section_algorithm_manipulation(self, algorithm, root):
        # Create container
        container = tk.LabelFrame(root, text="Algorithm Manipulation", background=root.cget("bg"))
        container.pack(fill=tk.X, padx=10, pady=(0, self.padding["regular"]))

        if(algorithm.view.create_section_manipulation(container) == False):
            container.destroy()

    def create_section_algorithm_presets(self, algorithm, root):
        # Create container
        container = tk.LabelFrame(root, text="Presets", background=root.cget("bg"))
        container.pack(fill=tk.X, padx=10, pady=(0, self.padding["regular"]))

        if(algorithm.view.create_section_presets(container) == False):
            container.destroy()

    ################################################################################
    # Overall Output Frame creation
    ################################################################################
    def create_output_frame(self, root):
        # Create a panel for the Matplotlib plot on the right side
        self.output_frame = tk.Frame(root, width=400, height=400, background="white")
        self.output_frame.pack(side=tk.LEFT)
        self.output_frame.pack_propagate(False)

        container = self.output_frame        

        # Create label header
        label_header = tk.Label(container, text=f"Generate Grid", font=("Helvetica", 12, "bold"), background=container.cget("bg"))
        label_header.pack(expand=True)
    

    ################################################################################
    # Helper methods
    ################################################################################
    def destroy_prev_canvas(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

    def show_output_grid(self, figure):
        # Clear previous canvas
        self.destroy_prev_canvas()

        for child in self.output_frame.winfo_children():
            child.destroy()

        # Embed the Matplotlib plot in the output frame
        self.canvas = FigureCanvasTkAgg(figure, master=self.output_frame) 
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def toggle_section_grid_manipulation(self, value):
        new_state = "normal" if value else "disabled"
        for container in self.widget_map[self.section_grid_manipulation].winfo_children():
            for child in container.winfo_children():
                if(value == False and child == self.widget_map[self.button_import]): 
                    continue
                child.configure(state=new_state)

    # On click button implementations
    def button_export_on_click(self):
        self.algorithm_view.view.button_export_on_click((self.algorithm_view.view.full_name).replace(" ", "_"))

    def button_import_on_click(self):
        self.algorithm_view.view.button_import_on_click()

    def button_flip_x_on_click(self):
        self.algorithm_view.view.button_flip_x_on_click()

    def button_flip_y_on_click(self):
        self.algorithm_view.view.button_flip_y_on_click() 

    def generate_button_on_click(self):
        self.toggle_section_grid_manipulation(True)
        self.algorithm_view.view.generate_button_on_click(self.get_entry_value_bool(self.cbox_using_seed))

    def grade_button_on_click(self):
        # Proof of Concept
        roughness_grader = RoughnessGrader()
        raw_grid_figure = self.algorithm_view.view.get_raw_grid_figure()
        image_path = cv2.imread(self.generate_image_path(raw_grid_figure), cv2.IMREAD_UNCHANGED)
        print(f"Roughness:{roughness_grader.get_score(image_path)}")

    def button_screenshot_screen_on_click(self):
        # Get the Tkinter window dimensions
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Capture the screenshot using ImageGrab
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        # # Save the screenshot to a file
        self.show_screenshot_popup(screenshot)

    def button_screenshot_grid_on_click(self):
       # Create the "screenshots" folder if it doesn't exist
        screenshots_folder = "grid-screenshots"
        os.makedirs(screenshots_folder, exist_ok=True)

        # Get the current date and time
        current_datetime = datetime.now()
        time_stamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

        # Formulate the filename based on the timestamp
        file_name = f"{screenshots_folder}/{time_stamp}_Grid.png"
        
        # Create Image
        raw_grid_figure = self.algorithm_view.view.get_raw_grid_figure()
        grid_height = raw_grid_figure.shape[0]  
        grid_width = raw_grid_figure[0].shape[0]
        image = Image.fromarray(raw_grid_figure)

        # Determine the desired size of the image based on the grid size
        # Here we are setting a multiplier to increase the size of the image
        multiplier = 20
        desired_size = (grid_width * multiplier, grid_height * multiplier)

        # Resize the image to the desired size while maintaining the aspect ratio
        image = image.resize(desired_size, Image.Resampling.NEAREST)  # Use NEAREST for nearest-neighbor interpolation

        image.save(file_name)
        image.show()

    def show_screenshot_popup(self, screenshot):
        def save_screenshot():
            # Create the "screenshots" folder if it doesn't exist
            screenshots_folder = "screen-screenshots"
            os.makedirs(screenshots_folder, exist_ok=True)

            # Get the current date and time
            current_datetime = datetime.now()
            time_stamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

            # Formulate the filename based on the timestamp
            file_name = f"{screenshots_folder}/{time_stamp}_{self.algorithm_view.full_name.replace(' ', '_')}.png"
            
            # Save the screenshot to a file
            screenshot.save(file_name)
            popup.destroy()  # Close the popup after saving

        # Create a new Tkinter window
        popup = tk.Toplevel(self.root)
        popup.title("Screenshot Preview")

        container = tk.Frame(popup, bg="black")
        container.pack(fill=tk.BOTH, expand=True)

        # Add a label above the screenshot
        label = tk.Label(container, text="SCREENSHOT PREVIEW", font=("Helvetica", 14, "bold"), bg=container.cget("background"), fg="white")
        label.pack(fill=tk.BOTH, expand=True, pady=(self.padding["regular"],0))

        # Bottom container
        bottom_container = tk.Frame(popup, bg=container.cget("background"))
        bottom_container.pack(fill=tk.BOTH, expand=True)

        buttons_container = tk.Frame(bottom_container, bg=container.cget("background"))
        buttons_container.pack(pady=self.padding["regular"])

        button_discard = tk.Button(buttons_container, text=f"Discard", command=popup.destroy, width=12, height=2, background="#E6B0AA")
        button_discard.pack(side=tk.LEFT, padx=(0,25))

        button_save = tk.Button(buttons_container, text=f"Save", command=save_screenshot, width=12, height=2, background="#A9DFBF")
        button_save.pack(side=tk.RIGHT)

        # Convert the screenshot to a format that Tkinter can display
        screenshot_tk = ImageTk.PhotoImage(screenshot)

        # Display the screenshot in a Tkinter label
        screenshot_label = tk.Label(popup, image=screenshot_tk)
        screenshot_label.pack()

        # Keep a reference to the ImageTk object to prevent it from being garbage collected
        screenshot_label.image = screenshot_tk

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
    
