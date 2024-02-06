import os
import importlib
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageGrab, ImageTk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Tab:
    def __init__(self, full_name, nickname, color, view, order):
        self.full_name = full_name
        self.nickname = nickname
        self.color = color
        self.view = view
        self.order = order

class MainView:
    def __init__(self):
        self.canvas = None

        self.padding = {
            "small": 4,
            "regular": 8,
        }

        self.colors = {
            "gray-500": "#D5D8DC",
        }

        # Root 
        self.root = None

        # Frames
        self.input_frame = None
        self.output_frame = None

        # Map of widgets
        self.widget_map = {}

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
        self.button_screenshot_screen = "button_screenshot_screen"
        self.button_screenshot_grid = "button_screenshot_grid"

        # Padding variables
        self.small_padding_y = 5

        self.load_algorithms()

        self.create_window() # Create main window
        self.root.mainloop() # Start the Tkinter event loop


    def load_algorithms(self):
        self.tabs = []

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

            # Access class
            view_class = getattr(view_module, f'{algorithm}View', None)

            # Create Tab data object
            tab = Tab(full_name=algorithm_full_name, nickname=algorithm_nickname, view=view_class(self, algorithm_full_name), color=algorithm_color, order=algorithm_order)
            self.tabs.append(tab)

        # Order tabs accordingly
        self.tabs = sorted(self.tabs, key=lambda x: x.order)

        # Set algorithm view to first tab
        self.algorithm_view = self.tabs[0]

    ################################################################################
    # Getters for widget values
    ################################################################################
    # To-Do
    # Reduce getters to singular get_entry_value, leave handling of data types to type casting
    # Ex.) num = int(self.get_entry_value(entry_num))

    def get_entry_value_int(self, entry):
        return int(self.widget_map[entry].get())
    
    def get_entry_value_float(self, entry):
        return float(self.widget_map[entry].get())

    def get_entry_value_bool(self, entry):
        return bool(self.widget_map[entry].get())
    
    def get_entry_width(self):
        return int(self.widget_map[self.entry_width].get())
    
    def get_entry_height(self):
        return int(self.widget_map[self.entry_height].get())

    def get_entry_seed(self):
        return self.get_entry_value_int(self.entry_seed)

    ################################################################################
    # Setters for widgets
    ################################################################################
    def set_entry_seed(self, seed):
        previously_disabled = False
        if(str(self.widget_map[self.entry_seed].cget("state")).strip() == "readonly"):
            previously_disabled = True
            self.widget_map[self.entry_seed].config(state="normal")

        self.widget_map[self.entry_seed].delete(0, tk.END) 
        self.widget_map[self.entry_seed].insert(0, seed) 

        if(previously_disabled):
            self.widget_map[self.entry_seed].config(state="readonly")

    def set_entry_value(self, entry, value, state="normal"):
        self.widget_map[entry].delete(0, tk.END) 

        if(value != None):
            self.widget_map[entry].insert(0, value)


        self.widget_map[entry].configure(state=state)

    def toggle_widget_state(self, entry, new_state):
        self.widget_map[entry].config(state=new_state)

    ################################################################################
    # Helper Methods
    ################################################################################
    def destroy_prev_canvas(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

    def show_output_grid(self, figure):
        # Clear previous canvas
        self.destroy_prev_canvas()

        # Embed the Matplotlib plot in the output frame
        self.canvas = FigureCanvasTkAgg(figure, master=self.output_frame) 
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def button_screenshot_screen_on_click(self):
        # Get the Tkinter window dimensions
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Capture the screenshot using ImageGrab
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        # # Save the screenshot to a file
        # screenshot.save(file_name)
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
        image = image.resize(desired_size, Image.NEAREST)  # Use NEAREST for nearest-neighbor interpolation


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


    ################################################################################
    # General Individual Widget Creators
    ################################################################################
    def create_single_label(self, root, label_text, label):
        self.widget_map[label] = tk.Label(root, text=f"{label_text}", background=root.cget("background"))
        self.widget_map[label].pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------------------
    # Entry creators
    # ------------------------------------------------------------------------------
    # Single Entry
    def create_single_entry(self, root, label_text, entry, def_val=""):
        # Container frame
        container = tk.Frame(root, background=root.cget("background"))
        container.pack(fill=tk.BOTH, padx=(self.padding["small"],self.padding["regular"]), pady=(self.padding["small"]))

        # Add label to container
        label = tk.Label(container, text=f"{label_text}:", background=root.cget("background"))
        label.pack(side=tk.LEFT)

        # Add entry to container
        self.widget_map[entry] = ttk.Entry(container)
        self.widget_map[entry].pack(side=tk.RIGHT)
        self.widget_map[entry].insert(0, def_val) 

    # Dual Entry - Single label
    def create_dual_entry(self, root, label, entry_1, entry_2, def_val_1="", def_val_2=""):
        # Create container 
        container = tk.Frame(root, background=root.cget("background"))
        container.pack(fill=tk.BOTH, padx=(self.padding["small"],self.padding["regular"]), pady=(self.padding["small"]))

        # Create label
        label = tk.Label(container, text=f"{label}:", background=root.cget("bg"))
        label.pack(side=tk.LEFT)

        # Create container for double entries
        entry_container = tk.Frame(container, background=root.cget("bg"))
        entry_container.pack(side=tk.RIGHT)
        entry_container.columnconfigure(0, weight=0) 
        entry_container.columnconfigure(1, weight=0)

        # Add first entry
        self.widget_map[entry_1] = ttk.Entry(entry_container, width=8)
        self.widget_map[entry_1].pack(side=tk.LEFT)
        self.widget_map[entry_1].insert(0, def_val_1) 

        # Add second entry
        self.widget_map[entry_2] = ttk.Entry(entry_container, width=8)
        self.widget_map[entry_2].pack(side=tk.LEFT)
        self.widget_map[entry_2].insert(0, def_val_2)

    # ------------------------------------------------------------------------------
    # Checkbox creators
    # ------------------------------------------------------------------------------
    def create_single_checkbox(self, root, label, ctrl_var, def_val=False):
        # Instantiate control variable
        self.widget_map[ctrl_var] = tk.BooleanVar()
        self.widget_map[ctrl_var].set(def_val)

        # Container frame
        container = tk.Frame(root, background=root.cget("background"))
        container.pack(fill=tk.BOTH, padx=(self.padding["small"],self.padding["regular"]), pady=(0, self.padding["small"]))

        # Create checkbox and assign it the control variable
        checkbox = tk.Checkbutton(container, text=f"{label}:", variable=self.widget_map[ctrl_var], background=container.cget("bg"))
        checkbox.pack(side=tk.LEFT, fill=tk.BOTH)

    # ------------------------------------------------------------------------------
    # Button creators
    # ------------------------------------------------------------------------------
    # Single Button
    def create_button(self, root, label, button, on_click, width=None, height=None, bg=None, state="normal"):
        # Create button
        self.widget_map[button] = tk.Button(root, text=f"{label}", command=on_click, state=state)
        if width is not None: self.widget_map[button].config(width=width)
        if height is not None: self.widget_map[button].config(height=height)
        if bg is not None: self.widget_map[button].config(bg=bg)
        self.widget_map[button].pack(fill=tk.BOTH, expand=True, padx=self.padding["small"], pady=self.padding["small"])

    # Dual Button
    def create_dual_buttons(self, root, label_1, button_1, on_click_1, label_2, button_2, on_click_2):
        # Create container
        container = tk.Frame(root, background=root.cget("bg"))
        container.pack(fill=tk.BOTH, expand=True, padx=self.padding["small"], pady=self.padding["small"])

        # Create left button
        self.widget_map[button_1] = tk.Button(container, text=f"{label_1}", command=on_click_1)
        self.widget_map[button_1].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,self.padding["small"]))
        
        # Create right button
        self.widget_map[button_2] = tk.Button(container, text=f"{label_2}", command=on_click_2)
        self.widget_map[button_2].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(self.padding["small"], 0))

    # ------------------------------------------------------------------------------
    # Radio Button creators
    # ------------------------------------------------------------------------------
    def create_radio_button(self, root, label, radio_button, variable, value, command=None):
        # Create container
        container = tk.Frame(root, background=root.cget("bg"))
        container.pack(fill=tk.BOTH, expand=True, padx=self.padding["small"], pady=(0, self.padding["small"]))

        # Create Radio Button
        self.widget_map[radio_button] = tk.Radiobutton(container, text=label, variable=variable, value=value, command=command, background=root.cget("bg"))
        self.widget_map[radio_button].pack(side=tk.LEFT, fill=tk.BOTH)

    # ------------------------------------------------------------------------------
    # Combined Widget creators
    # ------------------------------------------------------------------------------
    # Button-Entry
    def create_button_entry(self, root, label, button, on_click, entry, def_val, row_num):
        # Create container 
        container = ttk.Frame(root)
        container.pack(padx=self.padding["small"],pady=self.padding["small"])

        # Create button
        self.widget_map[button] = ttk.Button(container, text=f"{label}", command=on_click)
        self.widget_map[button].pack(side=tk.LEFT)

        # Create entry
        self.widget_map[entry] = tk.Entry(container)
        self.widget_map[entry].pack(side=tk.RIGHT)
        self.widget_map[entry].insert(0, def_val) 

    # Seed Entry
    def create_seed_entry(self, root):
        # Inner function
        def toggle_entry_seed_state():
            if self.widget_map[self.cbox_using_seed].get():
                self.widget_map[self.entry_seed].config(state="normal")
            else:
                self.widget_map[self.entry_seed].config(state="readonly")

        # Create container
        container = tk.Frame(root, background=root.cget("bg"))
        container.pack(padx=(0,self.padding["regular"]),pady=self.padding["small"])

        # Instantiate control variable
        self.cbox_using_seed = "cbox_use_seed"
        self.widget_map[self.cbox_using_seed] = tk.BooleanVar()
        self.widget_map[self.cbox_using_seed].set(False)

        # Create checkbox and assign it the control variable
        checkbox = tk.Checkbutton(container, text=f"Set Seed", variable=self.widget_map[self.cbox_using_seed], command=toggle_entry_seed_state, background=root.cget("bg"))
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
        container = tk.Frame(self.root)
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

    # Manipulation section creation  
    def create_section_grid_manipulation(self, root):
        # Create container
        self.section_grid_manipulation = "section_grid_manipulation"
        self.widget_map[self.section_grid_manipulation] = tk.LabelFrame(root, text="Grid Manipulation", background=root.cget("bg"))
        self.widget_map[self.section_grid_manipulation].pack(fill=tk.X, padx=self.padding["regular"], pady=self.padding["regular"])

        # Add Widgets
        self.create_dual_buttons(self.widget_map[self.section_grid_manipulation], label_1="Export Grid", button_1=self.button_export, on_click_1=self.button_export_on_click, 
                                            label_2="Import Grid", button_2=self.button_import, on_click_2=self.button_import_on_click)
        self.create_dual_buttons(self.widget_map[self.section_grid_manipulation], label_1="Flip X Axis", button_1=self.button_flip_x, on_click_1=self.button_flip_x_on_click, 
                                            label_2="Flip Y Axis", button_2=self.button_flip_y, on_click_2=self.button_flip_y_on_click)
        
        # Disable all buttons by default, (Grid hasn't been generated)
        self.toggle_section_grid_manipulation(False)

    def toggle_section_grid_manipulation(self, value):
        new_state = "normal" if value else "disabled"
        for container in self.widget_map[self.section_grid_manipulation].winfo_children():
            for child in container.winfo_children():
                if(value == False and child == self.widget_map[self.button_import]): 
                    continue
                child.configure(state=new_state)

    # Generation section creation  
    def create_section_grid_generation(self, root):
        # Create container
        container = tk.Frame(root, background=root.cget("bg"))
        container.pack(fill=tk.X, padx=self.padding["small"])

        # Add Widgets
        self.create_button(container, "GENERATE", self.button_generate, on_click=self.generate_button_on_click, height=2, bg="#D6DBDF")
        self.create_button(container, "SCREENSHOT SCREEN", self.button_screenshot_screen, on_click=self.button_screenshot_screen_on_click, height=2, bg="#F8F9F9")
        self.create_button(container, "SCREENSHOT GRID", self.button_screenshot_grid, on_click=self.button_screenshot_grid_on_click, height=2, bg="#F8F9F9")

    def generate_button_on_click(self):
        self.toggle_section_grid_manipulation(True)
 
        # try:
            # Run algorithm's button click implementation
        self.algorithm_view.view.generate_button_on_click(self.get_entry_value_bool(self.cbox_using_seed))
        
        # except Exception as error:
        #     messagebox.showerror("Error", error)

    def button_export_on_click(self):
        self.algorithm_view.view.button_export_on_click((self.algorithm_view.view.full_name).replace(" ", "_"))

    def button_import_on_click(self):
        self.algorithm_view.view.button_import_on_click()

    def button_flip_x_on_click(self):
        self.algorithm_view.view.button_flip_x_on_click()

    def button_flip_y_on_click(self):
        self.algorithm_view.view.button_flip_y_on_click()   

    # ------------------------------------------------------------------------------
    # Specific Input Frame Creation
    # ------------------------------------------------------------------------------
    def create_specific_frame(self, root):
        # Function to switch view based on selected tab
        def switch_view(event):
            selected_tab_index = container.index(container.select())
            self.algorithm_view = self.tabs[selected_tab_index]
            self.widget_map[self.button_generate].config(command=self.generate_button_on_click)
            # print(f"changed tab! : {self.tabs[selected_tab_index].full_name}")

        # Create notebook tab style
        style = ttk.Style(root)
        style.configure('LeftTab.TNotebook', tabposition='wn', background=self.colors["gray-500"])

        # Create container
        container = ttk.Notebook(root, style='LeftTab.TNotebook')
        container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        container.bind("<<NotebookTabChanged>>", switch_view)

        # Create tabs dynamically
        for tab in self.tabs:
            self.create_tab(container, tab)

    def create_tab(self, root, tab):
        # Create container
        container = tk.Frame(self.root, bg=tab.color)
        container.pack(side=tk.LEFT)

        # Create label header
        label_header = tk.Label(container, text=f"{tab.full_name}", font=("Helvetica", 12, "bold"), background=container.cget("bg"))
        label_header.pack()

        # Create section for specific algorithm
        self.create_section_algorithm_configuration(tab, container)
        self.create_section_algorithm_manipulation(tab, container)
        self.create_section_algorithm_presets(tab, container)

        # Add container to root
        root.add(container, text="{:^20}".format(tab.nickname))

    def create_section_algorithm_configuration(self, tab, root):
        # Create container
        container = tk.LabelFrame(root, text="Algorithm Configuration", background=root.cget("bg"))
        container.pack(fill=tk.X, padx=10, pady=(0, self.padding["regular"]))

        # Create algorithm section and add to container
        tab.view.create_section_configuration(container)

    def create_section_algorithm_manipulation(self, tab, root):
        # Create container
        container = tk.LabelFrame(root, text="Algorithm Manipulation", background=root.cget("bg"))
        container.pack(fill=tk.X, padx=10, pady=(0, self.padding["regular"]))

        if(tab.view.create_section_manipulation(container) == False):
            container.destroy()

    def create_section_algorithm_presets(self, tab, root):
        # Create container
        container = tk.LabelFrame(root, text="Presets", background=root.cget("bg"))
        container.pack(fill=tk.X, padx=10, pady=(0, self.padding["regular"]))

        if(tab.view.create_section_presets(container) == False):
            container.destroy()

    ################################################################################
    # Overall Output Frame creation
    ################################################################################
    def create_output_frame(self, root):
        # Create a panel for the Matplotlib plot on the right side
        self.output_frame = tk.Frame(root)
        self.output_frame.pack(side=tk.LEFT)
    

    ################################################################################
    # Main Window
    ################################################################################
    def create_window(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Cave Generation")

        # Create input and output frames
        self.create_input_frame(self.root)
        self.create_output_frame(self.root)

view = MainView()
