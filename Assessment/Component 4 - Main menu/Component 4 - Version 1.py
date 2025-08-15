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
        
        # Generate main window container
        self.main_container = Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky="NESW")
        
        # Themes
        # This will open up the themes json file
        with open("../data/theme_config.json") as f:
            theme_config_json = json.load(f)              
        
        chosen_theme_name = theme_config_json["chosen_theme"] # Find the name of the theme that the user has laste selected
        
        chosen_theme_details = theme_config_json[chosen_theme_name] # Find the details of that theme.
        
        # Set the theme related variables to that theme
        self.bg = chosen_theme_details["bg"]
        self.heading_bg = chosen_theme_details["heading_bg"]
        self.heading_txt = chosen_theme_details["heading_txt"]
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
    
    
    def create_HomePageFrame(self):
        '''Creates homepage frame'''
        self.home_page_frame = Frame(self.main_container, bg = self.bg)
        self.home_page_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading
        self.home_page_frame_heading = Label(self.home_page_frame,
                                             text = "Virtual cookbook",
                                             bg = self.heading_bg,
                                             fg = self.heading_txt)
        self.home_page_frame_heading.grid(row = 0, column = 0,
                                          sticky = "NESW",
                                          columnspan = 2)
        
        # Create and pack view recipes button
        self.home_page_frame_viewbutt = Button(self.home_page_frame,
                                               text = "View recipes")
        self.home_page_frame_viewbutt.grid(row = 1, column = 0, sticky = "NESW",
                                           columnspan = 2)
        
        # Create and pack add recipes button
        self.home_page_frame_addbutt = Button(self.home_page_frame,
                                              text = "Add recipes")
        self.home_page_frame_addbutt.grid(row = 2, column = 0, sticky = "NESW",
                                          columnspan = 2)
        
        # Create and pack edit recipes button
        self.home_page_frame_editbutt = Button(self.home_page_frame,
                                               text = "Edit recipes")
        self.home_page_frame_editbutt.grid(row = 3, column = 0, sticky = "NESW",
                                           columnspan = 2)
        
        # Create and pack setting button
        self.home_page_frame_settingsbutt = Button(self.home_page_frame,
                                                   text = "Settings",
                                                   command=lambda: self.show_frame("SettingsFrame"))
        self.home_page_frame_settingsbutt.grid(row = 4, column = 0, 
                                               sticky = "NESW")
        
        # Create and pack quit button
        self.home_page_frame_quitbutt = Button(self.home_page_frame,
                                               text = "Quit program",
                                               command = self.quit_program)
        self.home_page_frame_quitbutt.grid(row = 4, column = 1,
                                           sticky = "NESW")
        
        return self.home_page_frame
  

    def create_SettingsFrame(self):
        '''Creates the settings window'''
        self.settings_frame = Frame(self.main_container)
        self.settings_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading
        self.settings_frame_heading = Label(self.settings_frame,
                                            text = "Settings")
        self.settings_frame_heading.grid(row = 0, column = 0, sticky = "NESW",
                                         columnspan = 2)
        
        # Create and pack subheading "Change theme"
        self.settings_frame_subhead1 = Label(self.settings_frame,
                                            text = "Change theme:")
        self.settings_frame_subhead1.grid(row = 1, column = 0,
                                          sticky = "NESW")
        
        # Create and pack combobox for changing theme
        self.settings_frame_combobox1 = ttk.Combobox(self.settings_frame,
                                                     state = "readonly")
        self.settings_frame_combobox1.grid(row = 1, column = 1,
                                           sticky = "NESW")
        
        # Create and pack back button
        self.settings_frame_backbutt = Button(self.settings_frame,
                                              text = "Back",
                                              command=lambda: self.show_frame("HomePageFrame"))
        self.settings_frame_backbutt.grid(row = 2, column = 0,
                                          sticky = "NESW",
                                          columnspan = 2)
        
        return self.settings_frame
    
# Main program
if __name__ == "__main__":
    app = Program()
    app.run()
    
    
    #"Dark theme": {"bg": "#9c9c9c", "button_bg": "#ff9c9c", "button_txt": "#82f7ff"}