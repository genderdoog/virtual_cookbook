"""
Component 1: Viewing recipes

Created by: Matthew C
Created on: 22/07/2025

Version 1: Output to python shell
Version 2: Output to GUI - only specified recipe
Version 3: User can pick what recipe they want
Version 4: Resizes to window size
Version 5: No longer crashes when there are no recipes present, theming support
"""

import json
import random # For random recipe button
from tkinter import *
from tkinter import ttk

class Program:
    
    
    def __init__(self):
        '''Setup the GUI'''
        
        # Initialise window settings
        self.root = Tk()
        self.root.title("Component 1 - Version 5")
        
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
        
        # Initialise strings used to output recipe information
        self.recipe_name = StringVar()
        self.name_of_author_source = StringVar()
        self.recipe_info = StringVar()
        self.recipe_ingredients = StringVar()
        self.recipe_instructions = StringVar()
        
        # Set up timer textvariable for timer
        self.recipe_timer = StringVar()
        
        # Create dictionary to store what windows are in our program
        self.windows = {}
        
        # Creating windows in our GUI
        self.windows["HomeChoosingToViewRecipeFrame"] = self.create_HomeChoosingToViewRecipeFrame()
        self.windows["ShowRecipeFrame"] = self.create_ShowRecipeFrame("do_not_delete") # To make program run, we first to parse in blank data 
        
        # Show choosing recipe frame first when program is started
        self.show_frame("HomeChoosingToViewRecipeFrame")
        
        
    def show_frame(self, name):
        '''Show a frame, then bring it to the top'''
        frame = self.windows[name]
        frame.tkraise()
        
        
    def run(self):
        '''Run program'''
        self.root.mainloop()
        
        
    def run_timer(self):
        '''Runs the timer of a recipe'''
        self.recipe_timer.set(f"{self.timer_in_sec // 60}:{self.timer_in_sec % 60}")
        self.timer_in_sec -= 1
        
    
    def create_HomeChoosingToViewRecipeFrame(self):
        '''Menu which allows user to pick and choose a recipe'''
        # Create choose recipe frame window
        self.home_choosing_to_view_recipe_frame = Frame(self.main_container, 
                                                        bg = self.bg)
        self.home_choosing_to_view_recipe_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.home_choosing_to_view_recipe_frame.columnconfigure([0], minsize=150)
        self.home_choosing_to_view_recipe_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.home_choosing_to_view_recipe_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(1): # 2 column
            self.home_choosing_to_view_recipe_frame.grid_columnconfigure(j, weight=1)        
        
        # This will open up the dictionary which stores the actual name given by the user, and the name of the folder.
        with open("../data/recipe_index.json") as f:
            dict_recipes_combobox = json.load(f)
        
        list_recipes_combobox_name = list(dict_recipes_combobox.keys()) # Creates a list of the non-folder names of the recipes
        list_recipes_folder_name = list(dict_recipes_combobox.values()) # Creates a list which is of the folder type names of each recipe (used for random recipe button)
        
        # Create and pack combo box
        self.home_choosing_to_view_recipe_frame_combobox = ttk.Combobox(self.home_choosing_to_view_recipe_frame, 
                                                   state = "readonly",
                                                   values = list_recipes_combobox_name)
        self.home_choosing_to_view_recipe_frame_combobox.current(0) # Ensures that the first recipe is auto selected
        self.home_choosing_to_view_recipe_frame_combobox.grid(row = 0, column = 0, 
                                                    sticky = "NESW",
                                                    padx = 10, pady = 10)
        
        # Create and pack button which will change the view recipes frame
        self.home_choosing_to_view_recipe_frame_viewbutt = Button(self.home_choosing_to_view_recipe_frame, 
                                            # We want to parse in the name of the folder which holds the image and json of the recipe, hence we use the value of the dictionary
                                            text = "View recipe", 
                                            command=lambda: self.create_ShowRecipeFrame(dict_recipes_combobox[self.home_choosing_to_view_recipe_frame_combobox.get()]),
                                            bg = self.button_bg,
                                            fg = self.button_txt) 
        self.home_choosing_to_view_recipe_frame_viewbutt.grid(row = 1, column = 0, 
                                                              sticky="NESW",
                                                              padx = 10,
                                                              pady = 10)
        
        # Similar to the view recipe button, except it uses a random item from the list "list_recipes_folder_name"
        self.home_choosing_to_view_recipe_frame_ranbutt = Button(self.home_choosing_to_view_recipe_frame, 
                                            text = "Pick a random recipe for me!",
                                            command=lambda: self.create_ShowRecipeFrame(random.choice(list_recipes_folder_name)),
                                            bg = self.button_bg,
                                            fg = self.button_txt)
        self.home_choosing_to_view_recipe_frame_ranbutt.grid(row = 2, column = 0, 
                                                sticky = "NESW", padx = 10,
                                                pady = 10)
        
        # Create and pack back button
        self.home_choosing_to_view_recipe_frame_backbutt = Button(self.home_choosing_to_view_recipe_frame,
                                                                  text = "Back",
                                                                  bg = self.button_bg,
                                                                  fg = self.button_txt)
        self.home_choosing_to_view_recipe_frame_backbutt.grid(row = 3, column = 0,
                                                              sticky = "NESW",
                                                              padx = 10, 
                                                              pady = 10)
                                            
        
        return self.home_choosing_to_view_recipe_frame
    
    
    def create_ShowRecipeFrame(self, recipe_folder_name):
        '''Creates recipe frame for chosen recipe'''
        # Creates frame for each widget in recipe frame
        self.show_recipe_frame = Frame(self.main_container, bg = self.bg)
        self.show_recipe_frame.grid(row=0, column=0, sticky="NESW")
        
        # Used in conjunction with sticky to make it fill the window
        # First column, which displays 
        
        self.show_recipe_frame.columnconfigure([0,1,2], minsize = 420) # Formatting for first 3 columns       
        self.show_recipe_frame.columnconfigure(3, minsize = 100) # Formatting for last column (timer)
        
        self.show_recipe_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.show_recipe_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(4): # 4 columns
            self.show_recipe_frame.grid_columnconfigure(j, weight=1)
        
        # Open current recipe information from info.json file
        with open("../data/" + recipe_folder_name + "/info.json") as f:
            current_recipe = json.load(f)
    
        # Show recipe name
        # Get information from json file
        self.recipe_name.set(current_recipe["name"])
        
        # Create then pack heading
        self.show_recipe_frame_heading = Label(self.show_recipe_frame, 
                                          textvariable=self.recipe_name, 
                                          bg = self.heading_bg, 
                                          fg = self.heading_txt,
                                          font = "Verdana 20 bold")
        self.show_recipe_frame_heading.grid(row = 0, column = 0, 
                                            sticky = "NESW",
                                            padx = 10, pady = 10)
        
        # Show image
        self.show_recipe_frame_image = PhotoImage(file="../data/" + recipe_folder_name + "/image.png") # Create image widget
        
        # Scaling for image 
        # Get width and height of image
        image_height_pixels = self.show_recipe_frame_image.height()
        image_width_pixels = self.show_recipe_frame_image.width()
        
        # Find the scale factor, based on the size of the image
        result_height = image_height_pixels // 500
        result_width = image_width_pixels // 600
        
        # Find the final scale factor, which we will use with .subsample()
        scale_factor = result_height + result_width
        
        self.show_recipe_frame_image = self.show_recipe_frame_image.subsample(scale_factor) # Resizes image to be smaller
        # Create then show widget with the image inside
        self.show_recipe_frame_image_frame = Label(self.show_recipe_frame, image = self.show_recipe_frame_image, 
                                                   bg = self.subheading_bg,
                                                   fg = self.subheading_txt)
        self.show_recipe_frame_image_frame.grid(row = 1, column = 0, 
                                                sticky = "NESW",
                                                padx = 10, pady = 10)
        
        # Showing other recipe information
        self.building_recipe_info = "" # Create a temporary string so that we can add info to the textbox of the recipe
        
        # Concatnate recipe information, so that info is stored all in one string
        self.building_recipe_info += f"Author/source: {current_recipe['author/source']}\n"
        self.building_recipe_info += f"Prep time: {current_recipe['prep_time']}\n"
        self.building_recipe_info += f"Total time: {current_recipe['total_time']}\n"
        self.building_recipe_info += f"Serves: {current_recipe['serves']}"
        
        # Set the variable so then the Label widget can retrive this information via textvariable
        self.recipe_info.set(self.building_recipe_info)
        
        # Show recipe info box
        self.show_recipe_frame_recipe_info_textbox = Label(self.show_recipe_frame, 
                                         textvariable=self.recipe_info, 
                                         bg = self.subheading_bg,
                                         fg = self.subheading_txt,
                                         font = "Verdana 10")
        self.show_recipe_frame_recipe_info_textbox.grid(row = 2, column = 0, 
                                                        sticky="NESW",
                                                        padx = 10, pady = 10)
        
        # Show recipe ingredients
        self.building_recipe_ingredients = "" # Once again we set a temporary variable which strings will be joined together
        
        self.list_of_ingredients = current_recipe["ingredients"] # Find list of ingredients from json
        for each_item in range(len(self.list_of_ingredients)): # For each ingredient, we can add it to the temporary variable
            self.building_recipe_ingredients += f"{self.list_of_ingredients[each_item]}\n"       
        
        # Set the concatnated information into the textvariable
        self.recipe_ingredients.set(self.building_recipe_ingredients)
        
        # Show ingredients list
        self.show_recipe_frame_ingredients_textbox = Label(self.show_recipe_frame,
                                               textvariable=self.recipe_ingredients, 
                                               bg = self.subheading_bg,
                                               fg = self.subheading_txt, 
                                               justify = LEFT,
                                               wraplength = 400)
        self.show_recipe_frame_ingredients_textbox.grid(row = 0, column = 1, 
                                                        sticky="NESW",
                                                        rowspan = 3,
                                                        padx = 10, pady = 10)
        
        # Show recipe instructions
        self.building_recipe_instructions = "" # Create a temporary string which we will use to display the recipe instructions
        
        self.list_of_instructions = current_recipe["instructions"] # Create a variable which stores the instructions in a dictionary format
        
        # We now loop through each item in the dictionary
        for each_step in self.list_of_instructions:
            self.building_recipe_instructions += f"{each_step.title()}: {self.list_of_instructions[each_step]}\n\n"        
            
        # Set the textvariable which will be used in the label
        self.recipe_instructions.set(self.building_recipe_instructions)
        
        # Create then pack recipe instructions
        self.show_recipe_frame_instructions_textbox = Label(self.show_recipe_frame,
                                         textvariable=self.recipe_instructions,
                                         wraplength=400, justify = LEFT,
                                         bg = self.subheading_bg,
                                         fg = self.subheading_txt)
        self.show_recipe_frame_instructions_textbox.grid(row = 0, column = 2, 
                                                         sticky="NESW",
                                                         rowspan = 3,
                                                         padx = 10, pady = 10)
        
        # Getting timer information from json file
        self.timer_in_min = current_recipe["timer_set_to"] # Find the set timer in minutes from json file
        self.recipe_timer.set(self.timer_in_min) # Set the timer label to what is found in the json file
        self.timer_in_sec = self.timer_in_min * 60 # Convert minutes to seconds, which will be used for our calculations

        # Time textlabel
        self.show_recipe_frame_timer_label = Label(self.show_recipe_frame, textvariable=self.recipe_timer, 
                                 bg = self.subheading_bg,
                                 fg = self.subheading_txt)
        self.show_recipe_frame_timer_label .grid(row = 0, column = 3, 
                                                 sticky = "NESW", padx = 10,
                                                 pady = 10)
        
        # Timer start button
        #self.show_recipe_frame_timer_startbutt = Button(self.show_recipe_frame, 
                                                        #text = "Start timer",
                                                        #command=self.run_timer)
        #self.show_recipe_frame_timer_startbutt.grid(row = 1, column = 3, 
                                                    #sticky = "NESW",
                                                    #padx = 10, pady = 10)
        
        # Back button (return to main menu)
        self.show_recipe_frame_backbutt = Button(self.show_recipe_frame, text = "Back",
                                  command=lambda: self.show_frame("HomeChoosingToViewRecipeFrame"),
                                  bg = self.button_bg,
                                  fg = self.button_txt)
        self.show_recipe_frame_backbutt.grid(row = 3, column = 0, columnspan = 4, 
                                             sticky="NESW", padx = 10, pady = 10)        
        
        return self.show_recipe_frame
    
# Main program
if __name__ == "__main__":
    app = Program()
    app.run()