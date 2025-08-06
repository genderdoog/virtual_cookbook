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
from tkinter import ttk # For checkbox

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
        
        # Variables when user is adding ingredients
        self.display_quantity_name = StringVar()
        self.display_ingredients_list = StringVar()
        
        # Create dictionary to store what windows are in our program
        self.windows = {}
        
        # Creating windows for our GUI
        self.windows["HomeAddRecipesFrame"] = self.create_HomeAddRecipesFrame()
        self.windows["AskRecipeNameFrame"] = self.create_AskRecipeNameFrame()
        self.windows["AskRecipeAuthorSourceFrame"] = self.create_AskRecipeAuthorSourceFrame()
        self.windows["AskRecipePrepTimeFrame"] = self.create_AskRecipePrepTimeFrame()
        self.windows["AskRecipeTotalTimeFrame"] = self.create_AskRecipeTotalTimeFrame()
        self.windows["ShowCurrentIngredientsFrame"] = self.create_ShowCurrentIngredientsFrame()
        self.windows["AddIngredientQuantityTypeFrame"] = self.create_AddIngredientQuantityTypeFrame()
        self.windows["AddIngredientNameFrame"] = self.create_AddIngredientNameFrame()
        self.windows["AddIngredientAmountFrame"] = self.create_AddIngredientAmountFrame()
        
        # Show home frame first
        self.show_frame("HomeAddRecipesFrame")   
        
    def show_frame(self, name):
        '''Show a frame, then bring it to the top'''
        frame = self.windows[name]
        frame.tkraise()
       
        
    def run(self):
        '''Run program'''
        self.root.mainloop()
      
    def save_information(self, info):
        '''Adds argument to new_recipe_info'''
        pass
        
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
        
        # Create save button
        self.ask_recipe_name_frame_savebutt = Button(self.ask_recipe_name_frame,
                                                     text = "Save",
                                                     command=lambda: self.save_information(self.ask_recipe_name_frame_textbox.get()))
        self.ask_recipe_name_frame_savebutt.grid(row = 2, column = 1, sticky = "NESW")
        
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
                                                          text = "Next",
                                                          command=lambda: self.show_frame("AskRecipeTotalTimeFrame"))
        self.ask_recipe_prep_time_frame_nextbutt.grid(row = 2, column = 0,
                                                      sticky = "NESW")
        
        return self.ask_recipe_prep_time_frame
    
    
    def create_AskRecipeTotalTimeFrame(self):
        '''Creates window which asks user for total time for recipe'''
        self.ask_recipe_total_time_frame = Frame(self.main_container)
        self.ask_recipe_total_time_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading widget
        self.ask_recipe_total_time_frame_heading = Label(self.ask_recipe_total_time_frame,
                                                         text = "How many people does this recipe serve?")
        self.ask_recipe_total_time_frame_heading.grid(row = 0, column = 0,
                                                      sticky = "NESW")
        
        # Create and pack entry box
        self.ask_recipe_total_time_frame_textbox = Entry(self.ask_recipe_total_time_frame)
        self.ask_recipe_total_time_frame_textbox.grid(row = 1, column = 0, 
                                                      sticky = "NESW")
        
        # Create and pack next button
        self.ask_recipe_total_time_frame_nextbutt = Button(self.ask_recipe_total_time_frame,
                                                           text = "Next",
                                                           command=lambda: self.show_frame("ShowCurrentIngredientsFrame"))
        self.ask_recipe_total_time_frame_nextbutt.grid(row = 2, column = 0,
                                                       sticky = "NESW")
        
        return self.ask_recipe_total_time_frame
    
    def create_ShowCurrentIngredientsFrame(self):
        '''Shows current ingredients added to new recipe'''
        # Setting up frame
        self.show_current_ingredients_frame = Frame(self.main_container)
        self.show_current_ingredients_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading widget
        self.show_current_ingredients_frame_heading = Label(self.show_current_ingredients_frame,
                                                            text = "Current ingredients")
        self.show_current_ingredients_frame_heading.grid(row = 0, column = 0,
                                                         sticky = "NESW",
                                                         columnspan = 2)
        
        
        # Create and pack "current list of ingredients"
        self.show_current_ingredients_frame_list = Label(self.show_current_ingredients_frame,
                                                         textvariable = self.display_ingredients_list)
        self.show_current_ingredients_frame_list.grid(row = 1, column = 0,
                                                      sticky = "NESW")
        
        # Create and pack "add ingredients" button
        self.show_current_ingredients_frame_addbutt = Button(self.show_current_ingredients_frame,
                                                             text = "Add",
                                                             command=lambda: self.show_frame("AddIngredientQuantityTypeFrame"))
        self.show_current_ingredients_frame_addbutt.grid(row = 2, column = 0,
                                                         sticky = "NESW")
        
        # Create and pack "next" button
        self.show_current_ingredients_frame_nextbutt = Button(self.show_current_ingredients_frame,
                                                              text = "Next")
        self.show_current_ingredients_frame_nextbutt.grid(row = 2, column = 1,
                                                          sticky = "NESW")
        
        return self.show_current_ingredients_frame
        
        
    def create_AddIngredientQuantityTypeFrame(self):
        '''Asks user for ingredient quantity type'''
        self.add_ingredient_quantity_type_frame = Frame(self.main_container)
        self.add_ingredient_quantity_type_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create heading and pack heading
        self.add_ingredient_quantity_type_frame_heading = Label(self.add_ingredient_quantity_type_frame,
                                                                text = "Enter quantity type:")
        self.add_ingredient_quantity_type_frame_heading.grid(row = 0, column = 0,
                                                             sticky = "NESW")
        
        # This will open up the dictionary which stores all the valid quantity types, used for the combo box
        with open("../data/quantity_types.json") as f:
            quantity_types_combobox = json.load(f)
            
        # Find all the keys in the dictionary and then put it in one list
        quantity_types_keys = list(quantity_types_combobox.keys())
        
        # Create and pack combo box 
        self.add_ingredient_quantity_type_frame_combobox = ttk.Combobox(self.add_ingredient_quantity_type_frame,
                                                                        state = "readonly",
                                                                        values = quantity_types_keys)
        self.add_ingredient_quantity_type_frame_combobox.grid(row = 1, column = 0,
                                                              sticky = "NESW")
        
        # Create and pack next button
        self.add_ingredient_quantity_type_frame_nextbutt = Button(self.add_ingredient_quantity_type_frame,
                                                                  text = "Next",
                                                                  command=lambda: self.show_frame("AddIngredientNameFrame"))
        self.add_ingredient_quantity_type_frame_nextbutt.grid(row = 2, column = 0,
                                                              sticky = "NESW")
        
        return self.add_ingredient_quantity_type_frame
    
    
    def create_AddIngredientNameFrame(self):
        '''Asks user for ingredient name when adding new ingredients'''
        self.add_ingredient_name_frame = Frame(self.main_container)
        self.add_ingredient_name_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading
        self.add_ingredient_name_frame_heading = Label(self.add_ingredient_name_frame,
                                                       text = "Enter name of ingredient:")
        self.add_ingredient_name_frame_heading.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack text box which stores name of ingredient
        self.add_ingredient_name_frame_textbox = Entry(self.add_ingredient_name_frame)
        self.add_ingredient_name_frame_textbox.grid(row = 1, column = 0,
                                                     sticky = "NESW")
        
        
        # Create and pack save button
        self.add_ingredient_name_frame_savebutt = Button(self.add_ingredient_name_frame,
                                                         text = "Save")
        self.add_ingredient_name_frame_savebutt.grid(row = 2, column = 1,
                                                     sticky = "NESW")
        
        # Create and pack next button
        self.add_ingredient_name_frame_nextbutt = Button(self.add_ingredient_name_frame,
                                                         text = "Next",
                                                         command=lambda: self.show_frame("AddIngredientAmountFrame"))
        self.add_ingredient_name_frame_nextbutt.grid(row = 2, column = 0,
                                                     sticky = "NESW")
        
        return self.add_ingredient_name_frame
    
    
    def create_AddIngredientAmountFrame(self):
        '''Asks user for the amount of that ingredient which they have chosen'''
        self.add_ingredient_amount_frame = Frame(self.main_container)
        self.add_ingredient_amount_frame.grid(row = 0, column = 0, sticky = "NESW")

        # Creates and packs heading
        self.add_ingredient_amount_frame_heading = Label(self.add_ingredient_amount_frame,
                                                         text = "Enter amount of this ingredient type ")
        self.add_ingredient_amount_frame_heading.grid(row = 0, column = 0, 
                                                      sticky = "NESW")
        
        # Creates and displays the name of the ingredient, entered in a previous page
        self.add_ingredient_amount_frame_quantityname = Label(self.add_ingredient_amount_frame,
                                                              textvariable = self.display_quantity_name)
        self.add_ingredient_amount_frame_quantityname.grid(row = 1, column = 0,
                                                           sticky = "NESW")
        
        # Creates and packs entrybox
        self.add_ingredient_amount_frame_textbox = Entry(self.add_ingredient_amount_frame)
        self.add_ingredient_amount_frame_textbox.grid(row = 2, column = 0, 
                                                      sticky = "NESW")
        
        # Creates and packs next button
        self.add_ingredient_amount_frame_nextbutt = Button(self.add_ingredient_amount_frame,
                                                           text = "Next",
                                                           command=lambda: self.show_frame("ShowCurrentIngredientsFrame"))
        self.add_ingredient_amount_frame_nextbutt.grid(row = 4, column = 0,
                                                       sticky = "NESW")
        
        return self.add_ingredient_amount_frame
    
    def testing(self):
        print("testing")
# Main program
if __name__ == "__main__":
    app = Program()
    app.run()