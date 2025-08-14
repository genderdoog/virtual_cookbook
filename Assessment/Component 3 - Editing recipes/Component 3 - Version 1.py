"""
Component 3: Editing recipes 

Created by: Matthew C
Created on: 14/08/25

Version 1: minimum viable product GUI
"""

import json
import shutil # File management
from tkinter import *
from tkinter import ttk # For checkbox

class Program:
    
    def __init__(self):
        '''Setup the GUI'''
        # Initialise window settings
        self.root = Tk()
        self.root.title("Component 3 - Version 1")
        
        # Generate main window container
        self.main_container = Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky="NESW")
        
        # Storing information
        self.edited_recipe_info = {}
        self.display_recipe_name_edit_homepage = StringVar()
        
        # Create dictionary to store what windows are in our program
        self.windows = {}
        
        # Creating windows for our GUI
        # Homepage 
        self.windows["HomeEditRecipesFrame"] = self.create_HomeEditRecipesFrame()
        
        # Homepage for a specific recipe
        self.windows["HomeEditSpecificRecipeFrame"] = self.create_HomeEditSpecificRecipeFrame()
        
        # Show home frame first when program starts
        self.show_frame("HomeEditRecipesFrame")
        
    
    def show_frame(self, name):
        '''Show a frame, then bring it to the top'''
        frame = self.windows[name]
        frame.tkraise()
        
    
    def run(self):
        '''Run program'''
        self.root.mainloop() 
    
    def find_selected_recipe(self):
        '''Once user has selected what recipe they want to edit and push the edit
        button, this will store the .json contents in self.edited_recipe_info, 
        and change the frame'''
        
        # This will open up the dictionary which stores the actual name given by the user, and the name of the folder.
        with open("../data/recipe_index.json") as f:
            dict_recipes_combobox = json.load(f)          
        
        # Find the name of the recipe as named in the directory
        directory_recipe_name = dict_recipes_combobox[self.home_edit_recipes_frame_combobox.get()] 
        
        # Set contents of that recipe into the dictionary self.edited_recipe_info
        with open("../data/" + directory_recipe_name + "/info.json") as f:
            self.edited_recipe_info = json.load(f)
         
        # Set the display name variable, so that it can be shown on the next page        
        self.display_recipe_name_edit_homepage.set(self.edited_recipe_info["name"])
        
        # Change frames
        self.show_frame("HomeEditSpecificRecipeFrame")
    
    def create_HomeEditRecipesFrame(self):
        '''Creates homepage frame for adding recipes'''
        self.home_edit_recipes_frame = Frame(self.main_container)
        self.home_edit_recipes_frame.grid(row = 0, column = 0, sticky = "NESW") 
        
        # Create and pack heading
        self.home_edit_recipes_frame_heading = Label(self.home_edit_recipes_frame,
                                                     text = "Edit recipes")
        self.home_edit_recipes_frame_heading.grid(row = 0, column = 0,
                                                  sticky = "NESW")
        
        # This will open up the dictionary which stores the actual name given by the user, and the name of the folder.
        with open("../data/recipe_index.json") as f:
            dict_recipes_combobox = json.load(f)        
        
        list_recipes_combobox_name = list(dict_recipes_combobox.keys()) # Used for the combobox   
        
        # Create and pack combobox
        self.home_edit_recipes_frame_combobox = ttk.Combobox(self.home_edit_recipes_frame,
                                                             state = "readonly",
                                                             values = list_recipes_combobox_name)
        self.home_edit_recipes_frame_combobox.grid(row = 1, column = 0,
                                                   sticky = "NESW")
        
        # Create and pack "edit!" button
        self.home_edit_recipes_frame_editbutt = Button(self.home_edit_recipes_frame,
                                                       text = "Edit!",
                                                       command = self.find_selected_recipe)
        self.home_edit_recipes_frame_editbutt.grid(row = 2, column = 0,
                                                   sticky = "NESW")
        
        return self.home_edit_recipes_frame
    
    
    def create_HomeEditSpecificRecipeFrame(self):
        '''This serves as the main page for when the user selects a recipe they 
        want to edit'''
        self.home_edit_specific_recipe_frame = Frame(self.main_container)
        self.home_edit_specific_recipe_frame.grid(row = 0, column = 0, 
                                                  sticky = "NESW")
        
        # Create and pack heading
        self.home_edit_specific_recipe_frame_heading = Label(self.home_edit_specific_recipe_frame,
                                                             text = "Editings details for recipe named:")
        self.home_edit_specific_recipe_frame_heading.grid(row = 0, column = 0,
                                                         sticky = "NESW")
        
        # Create and pack recipe name
        self.home_edit_specific_recipe_frame_displayname = Label(self.home_edit_specific_recipe_frame,
                                                                 textvariable = self.display_recipe_name_edit_homepage)

        self.home_edit_specific_recipe_frame_displayname.grid(row = 1, column = 0,
                                                              sticky = "NESW")
        
        # Create and pack delete recipe button
        self.home_edit_specific_recipe_frame_delbutt = Button(self.home_edit_specific_recipe_frame,
                                                              text = "Delete recipe")
        self.home_edit_specific_recipe_frame_delbutt.grid(row = 2, column = 0,
                                                          sticky = "NESW")
        
        return self.home_edit_specific_recipe_frame
    

# Main program
if __name__ == "__main__":
    app = Program()
    app.run()