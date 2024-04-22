import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageGrab, ImageTk
from ResourceManager import ResourceManager

class TabView:
    def __init__(self, root):
        self.root = root

        self.padding = {
            "small": 4,
            "regular": 8,
        }

        self.widget_map = {}

        self.list_algorithms = ResourceManager().get_fitted_algorithm_list(self)
        self.list_grade_metrics = ResourceManager().get_list_grade_metrics()

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
    
    def get_list_algorithms(self):
        return self.list_algorithms
    
    ################################################################################
    # Setters for widgets
    ################################################################################
    def set_entry_value(self, entry, value, state="normal"):
        self.widget_map[entry].delete(0, tk.END) 

        if(value != None):
            self.widget_map[entry].insert(0, value)


        self.widget_map[entry].configure(state=state)

    def toggle_widget_state(self, entry, new_state):
        self.widget_map[entry].config(state=new_state)

    def set_cbox(self, cbox, value):
        self.widget_map[cbox].set(value)

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
    def create_single_checkbox(self, root, label, ctrl_var, def_val=False, command=None):
        # Instantiate control variable
        self.widget_map[ctrl_var] = tk.BooleanVar()
        self.widget_map[ctrl_var].set(def_val)

        # Container frame
        container = tk.Frame(root, background=root.cget("background"))
        container.pack(fill=tk.BOTH, padx=(self.padding["small"],self.padding["regular"]), pady=(0, self.padding["small"]))

        # Create checkbox and assign it the control variable
        checkbox = tk.Checkbutton(container, text=f"{label}", variable=self.widget_map[ctrl_var], command=command, background=container.cget("bg"))
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
        self.widget_map[button].pack(fill=tk.BOTH, expand=True, padx=self.padding["small"], pady=(0, self.padding["regular"]))

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


    # ------------------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------------------
    def show_screenshot_popup(self, screenshot, name):
        def save_screenshot():
            # Parent folder
            parent_folder = "screenshots"

            # Define specific screenshots folder
            screenshots_folder = os.path.join(parent_folder, "screen-screenshots")
            os.makedirs(screenshots_folder, exist_ok=True)

            # Get the current date and time
            current_datetime = datetime.now()
            time_stamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

            # Make the filename based on the timestamp
            file_name = f"{screenshots_folder}/{time_stamp}_{name}.png"
            
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
        
    