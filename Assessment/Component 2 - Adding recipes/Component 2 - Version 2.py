"""
Component 2: Adding recipes

Created by: Matthew C
Created on: 30/07/2025

Version 1: Output to python shell
Version 2: minimum viable product GUI
"""

import json
import os
from tkinter import *
from tkinter import ttk # Checkbox

class Program:
    
    def __init__(self):
        '''Setup the GUI'''
        # Initialise window settings
        self.root = Tk()
        self.root.title("Component 2 - Version 2")
        
        # Generate main window container
        self.main_container = Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky="NESW")
        
        self.new_recipe_info = {} # Creates the main dictionary which we will then dump to a json file
        
        # Create dictionary to store what windows are in our program
        self.windows = {}
        
        # Creating windows for our GUI
        self.windows["HomeAddRecipesFrame"] = self.create_HomeAddRecipesFrame()
        self.windows["AskRecipeNameFrame"] = self.create_AskRecipeNameFrame()
        self.windows["AskRecipeAuthorSourceFrame"] = self.create_AskRecipeAuthorSourceFrame()
        self.windows["AskRecipePrepTimeFrame"] = self.create_AskRecipePrepTimeFrame()
        
        # Show home frame first
        self.show_frame("HomeAddRecipesFrame")   
        
    def show_frame(self, name):
        '''Show a frame, then bring it to the top'''
        frame = self.windows[name]
        frame.tkraise()
        
    def run(self):
        '''Run program'''
        self.root.mainloop()
        
    def create_HomeAddRecipesFrame(self):
        '''Creates homepage of adding recipes'''
        # Sets up home frame window
        self.home_add_recipes_frame = Frame(self.main_container)
        self.home_add_recipes_frame.grid(row = 0, column = 0, sticky = "NESW") 
        
        # Create button to start creating a new recipe
        self.add_new_recipebutt = Button(self.home_add_recipes_frame, 
                                     text = "Add new recipe", 
                                     command=lambda: self.show_frame("AskRecipeNameFrame"))
        self.add_new_recipebutt.grid(row = 0, column = 0, sticky = "NESW")
        
        return self.home_add_recipes_frame
    
    def create_AskRecipeNameFrame(self):
        '''Asks for recipe name'''
        # Sets up window
        self.ask_recipe_name_frame = Frame(self.main_container)
        self.ask_recipe_name_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Creating and packing heading widget
        self.ask_recipe_name_frame_heading = Label(self.ask_recipe_name_frame,
                                                   text = "Enter name of recipe:")
        self.ask_recipe_name_frame_heading.grid(row = 0, column = 0, sticky = "NESW")
        
        # Creating and packing text box
        self.ask_recipe_name_frame_textbox = Entry(self.ask_recipe_name_frame)
        self.ask_recipe_name_frame_textbox.grid(row = 1, column = 0, 
                                                sticky = "NESW")
        
        # Create next button
        self.ask_recipe_name_frame_nextbutt = Button(self.ask_recipe_name_frame,
                                                     text = "Next",
                                                     command=lambda: self.show_frame("AskRecipeAuthorSourceFrame"))
        self.ask_recipe_name_frame_nextbutt.grid(row = 2, column = 0, 
                                                sticky = "NESW")
        
        return self.ask_recipe_name_frame
    
    def create_AskRecipeAuthorSourceFrame(self):
        '''Window which asks user for author/source'''
        # Set up window
        self.ask_recipe_author_source_frame = Frame(self.main_container)
        self.ask_recipe_author_source_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading widget
        self.ask_recipe_author_source_frame_heading = Label(self.ask_recipe_author_source_frame,
                                                            text = "Enter author/source of recipe:")
        self.ask_recipe_author_source_frame_heading.grid(row = 0, column = 0,
                                                         sticky = "NESW")
        
        # Create and pack text box
        self.ask_recipe_author_source_frame_textbox = Entry(self.ask_recipe_author_source_frame)
        self.ask_recipe_author_source_frame_textbox.grid(row = 1, column = 0,
                                                         sticky = "NESW" )
        
        # Create next button
        self.ask_recipe_author_source_frame_nextbutt = Button(self.ask_recipe_author_source_frame,
                                                              text = "Next",
                                                              command=lambda: self.show_frame("AskRecipePrepTimeFrame"))
        self.ask_recipe_author_source_frame_nextbutt.grid(row = 2, column = 0,
                                                          sticky = "NESW")
        
        return self.ask_recipe_author_source_frame
    
    def create_AskRecipePrepTimeFrame(self):
        '''Creates window to ask for prep time'''
        self.ask_recipe_prep_time_frame = Frame(self.main_container)
        self.ask_recipe_prep_time_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading widget
        self.ask_recipe_prep_time_frame_heading = Label(self.ask_recipe_prep_time_frame,
                                                        text = "Enter prep time:")
        self.ask_recipe_prep_time_frame_heading.grid(row = 0, column = 0,
                                                     sticky = "NESW")
        
        # Create and pack text box widget
        self.ask_recipe_prep_time_frame_textbox = Entry(self.ask_recipe_prep_time_frame)
        self.ask_recipe_prep_time_frame_textbox.grid(row = 1, column = 0,
                                                     sticky = "NESW")
        
        # Create next button
        self.ask_recipe_prep_time_frame_nextbutt = Button(self.ask_recipe_prep_time_frame,
                                                          text = "Next")
        self.ask_recipe_prep_time_frame_nextbutt.grid(row = 2, column = 0,
                                                      sticky = "NESW")
        
        return self.ask_recipe_prep_time_frame
        
# Main program
if __name__ == "__main__":
    app = Program()
    app.run()