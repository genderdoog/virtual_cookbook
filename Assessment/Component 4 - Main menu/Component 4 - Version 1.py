"""
Component 4: Main menu

Created by: Matthew C
Created on: 15/08/25

Version 1: minimum viable product GUI
"""

import json
from tkinter import *
from tkinter import ttk # For checkbox

class Program:
    
    def __init__(self):
        '''Setup the GUI'''
        # Initialise window settings
        self.root = Tk()
        self.root.title("Component 4 - Version 1")
        
        # Make the root window expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)        
        
        # Generate main window container
        self.main_container = Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky="NESW")
        
        # Make the main container expandable
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Themes
        # This will open up the themes json file
        with open("../data/theme_config.json") as f:
            theme_config_json = json.load(f)              
        
        chosen_theme_name = theme_config_json["chosen_theme"] # Find the name of the theme that the user has last selected
        
        chosen_theme_details = theme_config_json[chosen_theme_name] # Find the details of that theme.
        
        # Set the theme related variables to that theme
        self.bg = chosen_theme_details["bg"]
        self.heading_bg = chosen_theme_details["heading_bg"]
        self.heading_txt = chosen_theme_details["heading_txt"]
        self.subheading_bg = chosen_theme_details["subheading_bg"]
        self.subheading_txt = chosen_theme_details["subheading_txt"]
        self.button_bg = chosen_theme_details["button_bg"]
        self.button_txt = chosen_theme_details["button_txt"]
        
        
        # Create dictionary to store what windows are in our program
        self.windows = {}
        
        # Windows
        self.windows["HomePageFrame"] = self.create_HomePageFrame() # Main menu of program
        self.windows["SettingsFrame"] = self.create_SettingsFrame() # Settings frame
        
        # Show this frame when program first starts
        self.show_frame("HomePageFrame")
    
        
    def show_frame(self, name):
        '''Show a frame, then bring it to the top'''
        frame = self.windows[name]
        frame.tkraise()
        
    
    def run(self):
        '''Run program'''
        self.root.mainloop() 
     
     
    def quit_program(self):
        '''Closes program when user presses the quit button on the main menu'''
        self.root.destroy()        
    
    def set_theme(self, theme_name):
        '''After the user selects an item from the combobox, the user presses the
        save button which runs this code'''
        
        # This will open up the themes json file
        with open("../data/theme_config.json") as f:
            theme_config_json = json.load(f)              
        
        chosen_theme_details = theme_config_json[theme_name] # Find the details of that theme the user has selected
        
        # Set the theme related variables to that theme
        self.bg = chosen_theme_details["bg"]
        self.heading_bg = chosen_theme_details["heading_bg"]
        self.heading_txt = chosen_theme_details["heading_txt"]
        self.subheading_bg = chosen_theme_details["subheading_bg"]
        self.subheading_txt = chosen_theme_details["subheading_txt"]
        self.button_bg = chosen_theme_details["button_bg"]
        self.button_txt = chosen_theme_details["button_txt"]
        
        # Change the settings of each frame
        
        # Homepage frame
        self.home_page_frame.configure(bg = self.bg) 
        self.home_page_frame_heading.configure(bg = self.heading_bg,
                                               fg = self.heading_txt)
        self.home_page_frame_viewbutt.configure(bg = self.button_bg,
                                                fg = self.button_txt)
        self.home_page_frame_addbutt.configure(bg = self.button_bg,
                                               fg = self.button_txt)
        self.home_page_frame_editbutt.configure(bg = self.button_bg,
                                                fg = self.button_txt)
        self.home_page_frame_settingsbutt.configure(bg = self.button_bg,
                                                    fg = self.button_txt)
        self.home_page_frame_quitbutt.configure(bg = self.button_bg,
                                                fg = self.button_txt)
        
        # Settings frame
        self.settings_frame.configure(bg = self.bg)
        self.settings_frame_heading.configure(bg = self.heading_bg, 
                                              fg = self.heading_txt)
        self.settings_frame_subhead1.configure(bg = self.subheading_bg,
                                               fg = self.subheading_txt)
        self.settings_frame_savebutt.configure(bg = self.button_bg,
                                               fg = self.button_txt)
        self.settings_frame_backbutt.configure(bg = self.button_bg,
                                               fg = self.button_txt)
        
        
        # To make it persistent across application restarts, we change the first variable of the json file
        theme_config_json["chosen_theme"] = theme_name
        
        # Then write the theme file back
        with open("../data/theme_config.json", "w") as f:
            json.dump(theme_config_json, f, indent = 4)
            
    def create_HomePageFrame(self):
        '''Creates homepage frame'''
        self.home_page_frame = Frame(self.main_container, bg = self.bg)
        self.home_page_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.home_page_frame.columnconfigure([0,1], minsize=150)
        self.home_page_frame.rowconfigure([0,1,2,3,4], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(5): # 5 rows
            self.home_page_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.home_page_frame.grid_columnconfigure(j, weight=1)        
        
        # Create and pack heading
        self.home_page_frame_heading = Label(self.home_page_frame,
                                             text = "Virtual cookbook",
                                             bg = self.heading_bg,
                                             fg = self.heading_txt)
        self.home_page_frame_heading.grid(row = 0, column = 0,
                                          sticky = "NESW",
                                          columnspan = 2,
                                          padx = 10, pady = 10)
        
        # Create and pack view recipes button
        self.home_page_frame_viewbutt = Button(self.home_page_frame,
                                               text = "View recipes",
                                               bg = self.button_bg,
                                               fg = self.button_txt)
        self.home_page_frame_viewbutt.grid(row = 1, column = 0, sticky = "NESW",
                                           columnspan = 2, padx = 10, pady = 10)
        
        # Create and pack add recipes button
        self.home_page_frame_addbutt = Button(self.home_page_frame,
                                              text = "Add recipes",
                                              bg = self.button_bg,
                                              fg = self.button_txt)
        self.home_page_frame_addbutt.grid(row = 2, column = 0, sticky = "NESW",
                                          columnspan = 2, padx = 10, pady = 10)
        
        # Create and pack edit recipes button
        self.home_page_frame_editbutt = Button(self.home_page_frame,
                                               text = "Edit recipes",
                                               bg = self.button_bg,
                                               fg = self.button_txt)
        self.home_page_frame_editbutt.grid(row = 3, column = 0, sticky = "NESW",
                                           columnspan = 2, padx = 10, pady = 10)
        
        # Create and pack setting button
        self.home_page_frame_settingsbutt = Button(self.home_page_frame,
                                                   text = "Settings",
                                                   command=lambda: self.show_frame("SettingsFrame"),
                                                   bg = self.button_bg,
                                                   fg = self.button_txt)
        self.home_page_frame_settingsbutt.grid(row = 4, column = 0, 
                                               sticky = "NESW", 
                                               padx = 10, pady = 10)
        
        # Create and pack quit button
        self.home_page_frame_quitbutt = Button(self.home_page_frame,
                                               text = "Quit program",
                                               command = self.quit_program,
                                               bg = self.button_bg,
                                               fg = self.button_txt)
        self.home_page_frame_quitbutt.grid(row = 4, column = 1,
                                           sticky = "NESW", padx = 10,
                                           pady = 10)
        
        return self.home_page_frame
  

    def create_SettingsFrame(self):
        '''Creates the settings window'''
        self.settings_frame = Frame(self.main_container, bg = self.bg)
        self.settings_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.settings_frame.columnconfigure([0,1], minsize=150)
        self.settings_frame.rowconfigure([0,1,2,3,4,5], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(3): # 3 rows
            self.settings_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.settings_frame.grid_columnconfigure(j, weight=1)    
            
        # Create and pack heading
        self.settings_frame_heading = Label(self.settings_frame,
                                            text = "Settings", 
                                            bg = self.heading_bg,
                                            fg = self.heading_txt)
        self.settings_frame_heading.grid(row = 0, column = 0, sticky = "NESW",
                                         columnspan = 2, padx = 10, pady = 10)
        
        # Create and pack subheading "Change theme"
        self.settings_frame_subhead1 = Label(self.settings_frame,
                                            text = "Change theme:",
                                            bg = self.subheading_bg,
                                            fg = self.subheading_txt)
        self.settings_frame_subhead1.grid(row = 1, column = 0,
                                          sticky = "NESW",
                                          padx = 10, pady = 10)
        
        # This will open up the dictionary which stores the actual name given by the user, and the name of the folder.
        with open("../data/theme_config.json") as f:
            theme_config_json = json.load(f)        
        
        list_theme_names = list(theme_config_json.keys()) # Creates a list of the non-folder names of the recipes
        
        # Remove the first entry in the list as that is not supposed to be selectable to the user
        list_theme_names.pop(0)
        
        # Create and pack combobox for changing theme
        self.settings_frame_combobox1 = ttk.Combobox(self.settings_frame,
                                                     state = "readonly",
                                                     values = list_theme_names)
        self.settings_frame_combobox1.current() 
        self.settings_frame_combobox1.grid(row = 1, column = 1,
                                           sticky = "NESW",
                                           padx = 10, pady = 10)
        
        # Create and pack save button for settings frame
        self.settings_frame_savebutt = Button(self.settings_frame, 
                                              text = "Save theme details",
                                              bg = self.button_bg,
                                              fg = self.button_txt,
                                              command=lambda: self.set_theme(self.settings_frame_combobox1.get()))
        self.settings_frame_savebutt.grid(row = 2, column = 0, sticky = "NESW",
                                          columnspan = 2, padx = 10, pady = 10)
        
        # Create and pack back button
        self.settings_frame_backbutt = Button(self.settings_frame,
                                              text = "Back",
                                              command=lambda: self.show_frame("HomePageFrame"),
                                              bg = self.button_bg,
                                              fg = self.button_txt)
        self.settings_frame_backbutt.grid(row = 3, column = 0,
                                          sticky = "NESW",
                                          columnspan = 2, padx = 10, pady = 10)
        
        return self.settings_frame
    
# Main program
if __name__ == "__main__":
    app = Program()
    app.run()