"""
Component 1: Viewing recipes

Created by: Matthew C
Created on: 22/07/2025

Version 1: Output to python shell
Version 2: Output to GUI - only specified recipe
Version 3: User can pick what recipe they want
"""

import json
from tkinter import *
from tkinter import ttk

class Program:
    
    def __init__(self):
        '''Setup the GUI'''
        
        # Initialise window settings
        self.root = Tk()
        self.root.title("Component 1 - Version 3")
        
        # Generate main window container
        self.main_container = Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky="NESW")
        
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
        self.windows["ChoosingRecipeFrame"] = self.create_ChoosingRecipeFrame()
        self.windows["RecipeFrame"] = self.create_RecipeFrame()
        
        # Show choosing recipe frame first
        self.show_frame("ChoosingRecipeFrame")
        
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
        
        return
    
    def create_ChoosingRecipeFrame(self):
        '''Menu which allows user to pick and choose a recipe'''
        # Create choose recipe frame
        self.choose_recipe_frame = Frame(self.main_container)
        self.choose_recipe_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack combo box
        self.choose_recipe_combobox = ttk.Combobox(self.choose_recipe_frame, 
                                                   state = "readonly", values = 
                                                   ["testing"])
        self.choose_recipe_combobox.grid(row = 0, column = 0)
        
        self.choose_recipe_selbutt = Button(self.choose_recipe_frame, 
                                            text = "View recipe")
        self.choose_recipe_selbutt.grid(row = 1, column = 0)
                                            
        
        return self.choose_recipe_frame
    
    def create_RecipeFrame(self):
        '''Creates recipe frame for chosen recipe'''
        # Creates frame for each widget in recipe frame
        self.recipe_frame = Frame(self.main_container)
        self.recipe_frame.grid(row=0, column=0, sticky="NESW")
        
        # Open current recipe information from info.json file
        with open("../data/chocolate_chip_cookie/info.json") as f:
            current_recipe = json.load(f)
    
        # Show recipe name
        # Get information from json file
        self.recipe_name.set(current_recipe["name"])
        
        # Create then pack widget
        self.recipe_name_heading = Label(self.recipe_frame, 
                                          textvariable=self.recipe_name, bg="orange")
        self.recipe_name_heading.grid(row = 0, column = 0, sticky="NESW")
        
        # Show image
        self.recipe_image = PhotoImage(file="../data/chocolate_chip_cookie/image.png") # Create image widget
        self.recipe_image = self.recipe_image.subsample(12) # Resizes image to be smaller
        # Create then show widget with the image inside
        self.recipe_image_frame = Label(self.recipe_frame, image = self.recipe_image, bg="green")
        self.recipe_image_frame.grid(row = 1, column = 0, sticky = "NESW")
        
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
        self.recipe_info_textbox = Label(self.recipe_frame, 
                                         textvariable=self.recipe_info, bg="yellow")
        self.recipe_info_textbox.grid(row = 2, column = 0, sticky="NESW")
        
        # Show recipe ingredients
        self.building_recipe_ingredients = "" # Once again we set a temporary variable which strings will be joined together
        
        self.list_of_ingredients = current_recipe["ingredients"] # Find list of ingredients from json
        for each_item in range(len(self.list_of_ingredients)): # For each ingredient, we can add it to the temporary variable
            self.building_recipe_ingredients += f"{self.list_of_ingredients[each_item]}\n"       
        
        # Set the concatnated information into the textvariable
        self.recipe_ingredients.set(self.building_recipe_ingredients)
        
        # Show ingredients list
        self.recipe_ingredients_textbox = Label(self.recipe_frame,
                                               textvariable=self.recipe_ingredients, bg="red")
        self.recipe_ingredients_textbox.grid(row = 0, column = 1, sticky="NSEW",
                                             rowspan = 3)
        
        # Show recipe instructions
        self.building_recipe_instructions = "" # Create a temporary string which we will use to display the recipe instructions
        
        self.list_of_instructions = current_recipe["instructions"] # Create a variable which stores the instructions in a dictionary format
        
        # We now loop through each item in the dictionary
        for each_step in self.list_of_instructions:
            self.building_recipe_instructions += f"{each_step.title()}: {self.list_of_instructions[each_step]}\n\n"        
            
        # Set the textvariable which will be used in the label
        self.recipe_instructions.set(self.building_recipe_instructions)
        
        # Create then pack recipe instructions
        self.recipe_instructions_textbox = Label(self.recipe_frame,
                                         textvariable=self.recipe_instructions,
                                         wraplength=300, justify = LEFT)
        self.recipe_instructions_textbox.grid(row = 0, column = 2, sticky="NESW",
                                              rowspan = 3)
        
        # Timer label
        self.timer_in_min = current_recipe["timer_set_to"] # Find the set timer in minutes
        
        self.recipe_timer.set(self.timer_in_min)
        
        self.timer_in_sec = self.timer_in_min * 60 # Convert minutes to seconds

        
     
        
        
        self.timer_label = Label(self.recipe_frame, textvariable=self.recipe_timer, 
                                 bg="yellow")
        self.timer_label.grid(row = 0, column = 3, sticky = "NESW")
        
        self.timer_start_button = Button(self.recipe_frame, text = "Start timer", 
                                         command=self.run_timer)
        self.timer_start_button.grid(row = 1, column = 3, sticky = "NESW")
        
       
        return self.recipe_frame
    
# Main program
if __name__ == "__main__":
    app = Program()
    app.run()