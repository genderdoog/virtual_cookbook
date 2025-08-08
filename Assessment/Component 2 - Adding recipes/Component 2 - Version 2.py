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
        
        # Storing information
        self.new_recipe_info = {} # Creates the main dictionary which we will then dump to a json file
        self.temp_ingredient_info = [] # This will store information which will then be concatnated to then be added to ingredient_info
        self.new_ingredient_info = [] # This is the final list of all ingredients, which will be added to new_recipe_info
        
        # When the user is adding ingredient amount, this info will be shown
        self.display_ingredient_name = StringVar() 
        self.display_ingredient_type = StringVar()
        
        # Create dictionary to store what windows are in our program
        self.windows = {}
        
        # Creating windows for our GUI
        # Homepage
        self.windows["HomeAddRecipesFrame"] = self.create_HomeAddRecipesFrame()
        
        # Getting preliminary information
        self.windows["AskRecipeNameFrame"] = self.create_AskRecipeNameFrame()
        self.windows["AskRecipeAuthorSourceFrame"] = self.create_AskRecipeAuthorSourceFrame()
        self.windows["AskRecipePrepTimeFrame"] = self.create_AskRecipePrepTimeFrame()
        self.windows["AskRecipeTotalTimeFrame"] = self.create_AskRecipeTotalTimeFrame()
        self.windows["AskRecipeHowManyServesFrame"] = self.create_AskRecipeHowManyServesFrame()
        
        # Adding ingredients
        self.windows["ShowCurrentIngredientsFrame"] = self.create_ShowCurrentIngredientsFrame()
        self.windows["AddIngredientQuantityTypeFrame"] = self.create_AddIngredientQuantityTypeFrame()
        self.windows["AddIngredientNameFrame"] = self.create_AddIngredientNameFrame()
        self.windows["AddIngredientAmountFrame"] = self.create_AddIngredientAmountFrame()
        self.windows["AddIngredientGenericTextFrame"] = self.create_AddIngredientGenericTextFrame()
        
        # Show home frame first when program starts
        self.show_frame("HomeAddRecipesFrame")   
        
    def show_frame(self, name):
        '''Show a frame, then bring it to the top'''
        frame = self.windows[name]
        frame.tkraise()
       
        
    def run(self):
        '''Run program'''
        self.root.mainloop()
      
      
    def save_information(self, data_type, info):
        '''When the users presses this button, it saves it to the main dictionary'''
        self.new_recipe_info[data_type] = info # Stores data_type name and value e.g. {"name": "chocolate chip cookie"} where name is data_type and chocolate chip cookie is info
        print(self.new_recipe_info) 
        
    def save_temp_ingredient_info(self, data_type, info):
        '''This is used to build the ingredients that the user adds'''
        # If user presses the save button when choosing quantity type
        if data_type == "quantity_type":
            self.temp_ingredient_info = [] # We will first blank out the list that stores the temp_ingredient info, in case user previously added a ingredient
            
            # Once again we open the quantity types json file so that we can append the apropriate end to the final string
            with open("../data/quantity_types.json") as f:
                quantity_types_combobox = json.load(f)
            
            try: # If the user wants to change their quantity type, after having pressed save
                self.temp_ingredient_info.pop(-1) # Remove the current quantity type
                self.temp_ingredient_info.append(quantity_types_combobox[info]) # Add the quantity type to the temporary ingredients dictionary
                self.display_ingredient_type.set(info) # This will be used on the page where they add the ingredient amount
                print(self.temp_ingredient_info)
           
            except IndexError: # If this is the first time the user is selecting a quantity type
                self.temp_ingredient_info.append(quantity_types_combobox[info]) 
                self.display_ingredient_type.set(info) # This will be used on the page where they add the ingredient amount
                print(self.temp_ingredient_info)
            
        # If user presses save button when entering the ingredient name
        elif data_type == "quantity_name":
            
            # If this is the first time the user is adding the name to the ingredient
            if len(self.temp_ingredient_info) == 1:
                self.temp_ingredient_info.append(info) # Add the name to the temp ingredient list
                self.display_ingredient_name.set(info) # This will be used on the next page when asking for quantity name
                print(self.temp_ingredient_info)
            
            # If user has changed their ingredient name after pressing save
            else:
                self.temp_ingredient_info.pop(-1) # Remove the old ingredient name
                self.temp_ingredient_info.append(info) # Add the new ingredient name to the temp list
                self.display_ingredient_name.set(info) # This will be used on the next page when asking for quantity name
                print(self.temp_ingredient_info)
                
            
        # If user presses save button when entering ingredient amount
        # This is special as we need to save it to the ingredient_info as well when the user presses save in this text
        elif data_type == "quantity_amount":
            try:
                info = int(info) # Turn the ingredient amount into a integer value
                
                if info <= 0: # If amount entered is less than 0, this is an invalid amount 
                    print("less than 0")
                
                else: # Amount entered is valid, so we now add it to temp_ingredient_info
                    if len(self.temp_ingredient_info) == 2: # If this is the first that the user saves their ingredient amount
                        self.temp_ingredient_info.append(info) # Add the quantity amount to the list
                        print(self.temp_ingredient_info)
                        final_ingredient = f"{self.temp_ingredient_info[2]}{self.temp_ingredient_info[0]} {self.temp_ingredient_info[1]}" # Concatnate ingredients info to form final ingredient line, which we will add to the temp_ingredient_info list
                        print(final_ingredient)
                        self.new_ingredient_info.append(final_ingredient) # Add the fully built ingredient line to the temp ingredient dictionary
                        print(self.new_ingredient_info)
                        
                    else: # If user has already saved their ingredient amount
                        self.temp_ingredient_info.pop(-1) # Removes old quantity value
                        self.temp_ingredient_info.append(info) # Add the new quantity amount to the list
                        print(self.temp_ingredient_info)
                        final_ingredient = f"{self.temp_ingredient_info[2]}{self.temp_ingredient_info[0]} {self.temp_ingredient_info[1]}" # Concatnate ingredients info to form final ingredient line, which we will add to the temp_ingredient_info list
                        print(final_ingredient)
                        self.new_ingredient_info.pop(-1) # Removes the old ingredient which user has decided to replace
                        self.new_ingredient_info.append(final_ingredient) # Add the fully built ingredient line to the temp ingredient dictionary
                        print(self.new_ingredient_info)                        
                    
            except ValueError: # If a letter is found in the ingredient amount
                if "/" in info: # Special case for entering fractions like 3/4
                    info = str(info) # Turn it into a string
                    
                    if len(self.temp_ingredient_info) == 2: # If this is the first that the user saves their ingredient amount
                        print("/detected, first time")
                        #self.temp_ingredient_info.append(info) # Add the quantity amount to the list
                        #final_ingredient = f"{self.temp_ingredient_info[2]}{self.temp_ingredient_info[0]} {self.temp_ingredient_info[1]}" # Concatnate ingredients info to form final ingredient line
                        #print(final_ingredient)
                        ##self.ingredient_info.append(final_ingredient)
                        ##print(self.ingredient_info)
                        
                    else: # If user has already saved their ingredient amount
                        print("/detected, notfirsttime")
                        #self.temp_ingredient_info.pop(-1) # Remove the current quantity amount
                        #self.temp_ingredient_info.append(info) # Add the new quantity amount 
                        #final_ingredient = f"{self.temp_ingredient_info[2]}{self.temp_ingredient_info[0]} {self.temp_ingredient_info[1]}" # Concatnate ingredients info to form final ingredient line
                        #print(final_ingredient)
                        ##self.ingredient_info.append(final_ingredient)
                        ##print(self.ingredient_info)                  
                
                else:
                    print("enter whole values only")
        
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
        '''Asks for recipe name window'''
        # Sets up window
        self.ask_recipe_name_frame = Frame(self.main_container)
        self.ask_recipe_name_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Creating and packing heading widget
        self.ask_recipe_name_frame_heading = Label(self.ask_recipe_name_frame,
                                                   text = "Enter name of recipe:")
        self.ask_recipe_name_frame_heading.grid(row = 0, column = 0, sticky = "NESW",
                                                columnspan = 2,)
        
        # Creating and packing text box
        self.ask_recipe_name_frame_textbox = Entry(self.ask_recipe_name_frame)
        self.ask_recipe_name_frame_textbox.grid(row = 1, column = 0,
                                                columnspan = 2,
                                                sticky = "NESW")
        
        # Create next button
        self.ask_recipe_name_frame_nextbutt = Button(self.ask_recipe_name_frame,
                                                     text = "Next",
                                                     command=lambda: self.show_frame("AskRecipeAuthorSourceFrame"))
        self.ask_recipe_name_frame_nextbutt.grid(row = 2, column = 0, 
                                                sticky = "NESW")
        
        # Create save button to store value in self.new_recipe_info
        self.ask_recipe_name_frame_savebutt = Button(self.ask_recipe_name_frame,
                                                     text = "Save",
                                                     command=lambda: self.save_information("name", self.ask_recipe_name_frame_textbox.get())) 
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
                                                         sticky = "NESW",
                                                         columnspan = 2)
        
        # Create and pack text box
        self.ask_recipe_author_source_frame_textbox = Entry(self.ask_recipe_author_source_frame)
        self.ask_recipe_author_source_frame_textbox.grid(row = 1, column = 0,
                                                         sticky = "NESW", 
                                                         columnspan = 2)
        
        # Create next button and pack next button
        self.ask_recipe_author_source_frame_nextbutt = Button(self.ask_recipe_author_source_frame,
                                                              text = "Next",
                                                              command=lambda: self.show_frame("AskRecipePrepTimeFrame"))
        self.ask_recipe_author_source_frame_nextbutt.grid(row = 2, column = 0,
                                                          sticky = "NESW")
        
        # Create and pack save button
        self.ask_recipe_author_source_frame_savebutt = Button(self.ask_recipe_author_source_frame,
                                                              text = "Save",
                                                              command=lambda: self.save_information("author/source", self.ask_recipe_author_source_frame_textbox.get()))
        self.ask_recipe_author_source_frame_savebutt.grid(row = 2, column = 1,
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
                                                     sticky = "NESW", 
                                                     columnspan = 2)
        
        # Create and pack text box widget
        self.ask_recipe_prep_time_frame_textbox = Entry(self.ask_recipe_prep_time_frame)
        self.ask_recipe_prep_time_frame_textbox.grid(row = 1, column = 0,
                                                     sticky = "NESW",
                                                     columnspan = 2)
        
        # Create and pack next button
        self.ask_recipe_prep_time_frame_nextbutt = Button(self.ask_recipe_prep_time_frame,
                                                          text = "Next",
                                                          command=lambda: self.show_frame("AskRecipeTotalTimeFrame"))
        self.ask_recipe_prep_time_frame_nextbutt.grid(row = 2, column = 0,
                                                      sticky = "NESW")
        
        # Create and pack save button
        self.ask_recipe_prep_time_frame_savebutt = Button(self.ask_recipe_prep_time_frame,
                                                          text = "Save",
                                                          command=lambda: self.save_information("prep_time", self.ask_recipe_prep_time_frame_textbox.get()))
        self.ask_recipe_prep_time_frame_savebutt.grid(row = 2, column = 1,
                                                      sticky = "NESW")
        
        return self.ask_recipe_prep_time_frame
    
    
    def create_AskRecipeTotalTimeFrame(self):
        '''Creates window which asks user for total time to make recipe'''
        self.ask_recipe_total_time_frame = Frame(self.main_container)
        self.ask_recipe_total_time_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading widget
        self.ask_recipe_total_time_frame_heading = Label(self.ask_recipe_total_time_frame,
                                                         text = "Enter total cooking time:")
        self.ask_recipe_total_time_frame_heading.grid(row = 0, column = 0,
                                                      sticky = "NESW", 
                                                      columnspan = 2)
        
        # Create and pack entry box so that user can enter how long in total it will take to make that recipe
        self.ask_recipe_total_time_frame_textbox = Entry(self.ask_recipe_total_time_frame)
        self.ask_recipe_total_time_frame_textbox.grid(row = 1, column = 0, 
                                                      sticky = "NESW",
                                                      columnspan = 2)
        
        # Create and pack next button, to move onto asking how many servings is this recipe for
        self.ask_recipe_total_time_frame_nextbutt = Button(self.ask_recipe_total_time_frame,
                                                           text = "Next",
                                                           command=lambda: self.show_frame("AskRecipeHowManyServesFrame"))
        self.ask_recipe_total_time_frame_nextbutt.grid(row = 2, column = 0,
                                                       sticky = "NESW")
        
        # Create and pack save button, to save total time required to make this recipe
        self.ask_recipe_total_time_frame_savebutt = Button(self.ask_recipe_total_time_frame,
                                                           text = "Save",
                                                           command=lambda: self.save_information("total_time", self.ask_recipe_total_time_frame_textbox.get()))
        self.ask_recipe_total_time_frame_savebutt.grid(row = 2, column = 1,
                                                       sticky = "NESW")
        
        return self.ask_recipe_total_time_frame
    
    def create_AskRecipeHowManyServesFrame(self):
        '''Creates window which allows user to input how many people this recipe serves'''
        self.ask_recipe_how_many_serves_frame = Frame(self.main_container)
        self.ask_recipe_how_many_serves_frame.grid(row = 0, column = 0,
                                                   sticky = "NESW")
        
        # Creates and packs heading widget
        self.ask_recipe_how_many_serves_frame_heading = Label(self.ask_recipe_how_many_serves_frame,
                                                              text = "How many people does this recipe serve?")
        self.ask_recipe_how_many_serves_frame_heading.grid(row = 0, column = 0,
                                                           sticky = "NESW",
                                                           columnspan = 2)
        
        # Creates and packs entry box for user to input number of servings
        self.ask_recipe_how_many_serves_frame_textbox = Entry(self.ask_recipe_how_many_serves_frame)
        self.ask_recipe_how_many_serves_frame_textbox.grid(row = 1, column = 0,
                                                           sticky = "NESW",
                                                           columnspan = 2)
        
        # Creates and packs next button, which will move onto asking for ingredients
        self.ask_recipe_how_many_serves_frame_nextbutt = Button(self.ask_recipe_how_many_serves_frame,
                                                                text = "Next",
                                                                command=lambda: self.show_frame("ShowCurrentIngredientsFrame"))
        self.ask_recipe_how_many_serves_frame_nextbutt.grid(row = 2, column = 0,
                                                            sticky = "NESW")
        
        # Creates and packs save button, to save current information into self.new_recipe_info
        self.ask_recipe_how_many_serves_frame_savebutt = Button(self.ask_recipe_how_many_serves_frame,
                                                                text = "Save",
                                                                command=lambda: self.save_information("serves", self.ask_recipe_how_many_serves_frame_textbox.get()))
        self.ask_recipe_how_many_serves_frame_savebutt.grid(row = 2, column = 1,
                                                            sticky = "NESW")
        
        return self.ask_recipe_how_many_serves_frame
    
    
    def create_ShowCurrentIngredientsFrame(self):
        '''Shows current ingredients added to new recipe'''
        # Setting up frame
        self.show_current_ingredients_frame = Frame(self.main_container)
        self.show_current_ingredients_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading widget
        self.show_current_ingredients_frame_heading = Label(self.show_current_ingredients_frame,
                                                            text = "Current ingredients:")
        self.show_current_ingredients_frame_heading.grid(row = 0, column = 0,
                                                         sticky = "NESW",
                                                         columnspan = 3)
        
        ## Create and pack "current list of ingredients"
        #self.show_current_ingredients_frame_list = Label(self.show_current_ingredients_frame,
                                                         #textvariable = self.new_ingredient_info)
        #self.show_current_ingredients_frame_list.grid(row = 1, column = 0,
                                                      #sticky = "NESW")
        
        # Create and pack "add ingredients" button
        self.show_current_ingredients_frame_addbutt = Button(self.show_current_ingredients_frame,
                                                             text = "Add",
                                                             command=lambda: self.show_frame("AddIngredientQuantityTypeFrame"))
        self.show_current_ingredients_frame_addbutt.grid(row = 2, column = 0,
                                                         sticky = "NESW")
        
        # Crreat and pack save button, which will add everything self.ingredient_info into self.new_recipe_info
        self.show_current_ingredients_frame_savebutt = Button(self.show_current_ingredients_frame,
                                                              text = "Save",
                                                              command=lambda: self.save_information("ingredients", self.new_ingredient_info))
        self.show_current_ingredients_frame_savebutt.grid(row = 2, column = 2,
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
                                                             sticky = "NESW",
                                                             columnspan = 2)
        
        # This will open up the dictionary which stores all the valid quantity types, used for the combo box
        with open("../data/quantity_types.json") as f:
            quantity_types_combobox = json.load(f)
            
        # Find all the keys in the dictionary and then put it in one list
        quantity_types_keys = list(quantity_types_combobox.keys())
        
        # Create and pack combo box 
        self.add_ingredient_quantity_type_frame_combobox = ttk.Combobox(self.add_ingredient_quantity_type_frame,
                                                                        state = "readonly", # So that user cannot add their own quantity values
                                                                        values = quantity_types_keys) # Set values to what is in the dictionary keys
        self.add_ingredient_quantity_type_frame_combobox.grid(row = 1, column = 0,
                                                              sticky = "NESW",
                                                              columnspan = 2)
        
        # Create and pack next button, to move onto asking the ingredient name
        self.add_ingredient_quantity_type_frame_nextbutt = Button(self.add_ingredient_quantity_type_frame,
                                                                  text = "Next",
                                                                  command=lambda: self.show_frame("AddIngredientNameFrame"))
        self.add_ingredient_quantity_type_frame_nextbutt.grid(row = 2, column = 0,
                                                              sticky = "NESW")
        
        # Create and pack save button, to save information to self.temp_ingredient_info
        self.add_ingredient_quantity_type_frame_savebutt = Button(self.add_ingredient_quantity_type_frame,
                                                                  text = "Save",
                                                                  command=lambda: self.save_temp_ingredient_info("quantity_type", self.add_ingredient_quantity_type_frame_combobox.get())) 
        self.add_ingredient_quantity_type_frame_savebutt.grid(row = 2, column = 1,
                                                             sticky = "NESW")
        
        return self.add_ingredient_quantity_type_frame

    
    def create_AddIngredientNameFrame(self):
        '''Asks user for ingredient name when adding new ingredients'''
        self.add_ingredient_name_frame = Frame(self.main_container)
        self.add_ingredient_name_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading
        self.add_ingredient_name_frame_heading = Label(self.add_ingredient_name_frame,
                                                       text = "Enter name of ingredient:")
        self.add_ingredient_name_frame_heading.grid(row = 0, column = 0, 
                                                    sticky = "NESW",
                                                    columnspan = 2)
        
        # Create and pack text box which stores name of ingredient
        self.add_ingredient_name_frame_textbox = Entry(self.add_ingredient_name_frame)
        self.add_ingredient_name_frame_textbox.grid(row = 1, column = 0,
                                                     sticky = "NESW",
                                                     columnspan = 2)
        
        # Create and pack save button
        self.add_ingredient_name_frame_savebutt = Button(self.add_ingredient_name_frame,
                                                         text = "Save",
                                                         command=lambda: self.save_temp_ingredient_info("quantity_name", self.add_ingredient_name_frame_textbox.get())) 
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
        self.add_ingredient_amount_frame_heading1 = Label(self.add_ingredient_amount_frame,
                                                         text = "Enter amount of this ingredient type ")
        self.add_ingredient_amount_frame_heading1.grid(row = 0, column = 0, 
                                                      sticky = "NESW",
                                                      columnspan = 2)
        
        # Creates and displays the name of the ingredient, entered in a previous page
        self.add_ingredient_amount_frame_quantityname = Label(self.add_ingredient_amount_frame,
                                                              textvariable = self.display_ingredient_name)
        self.add_ingredient_amount_frame_quantityname.grid(row = 1, column = 0,
                                                           sticky = "NESW",
                                                           columnspan = 2)
        
        # Creates and packs entrybox
        self.add_ingredient_amount_frame_textbox = Entry(self.add_ingredient_amount_frame)
        self.add_ingredient_amount_frame_textbox.grid(row = 2, column = 0, 
                                                      sticky = "NESW",
                                                      columnspan = 2)
        
        # Creates and packs heading for "in"
        self.add_ingredient_amount_frame_heading2 = Label(self.add_ingredient_amount_frame,
                                                          text = "in")
        self.add_ingredient_amount_frame_heading2.grid(row = 3, column = 0,
                                                       sticky = "NESW",
                                                       columnspan = 2)
        
        # Creates and displays quantity type of ingredient, entered on a previous page
        self.add_ingredient_amount_frame_quantitytype = Label(self.add_ingredient_amount_frame,
                                                              textvariable = self.display_ingredient_type)
        self.add_ingredient_amount_frame_quantitytype.grid(row = 4, column = 0,
                                                           sticky = "NESW",
                                                           columnspan = 2)
        
        # Creates and packs next button
        self.add_ingredient_amount_frame_nextbutt = Button(self.add_ingredient_amount_frame,
                                                           text = "Next",
                                                           command=lambda: self.show_frame("ShowCurrentIngredientsFrame"))
        self.add_ingredient_amount_frame_nextbutt.grid(row = 5, column = 0,
                                                       sticky = "NESW")
        
        # Creates and packs save button, which will add the quantity amount to the temp ingredient dictionary
        self.add_ingredient_amount_frame_savebutt = Button(self.add_ingredient_amount_frame,
                                                           text = "Save",
                                                           command=lambda: self.save_temp_ingredient_info("quantity_amount", self.add_ingredient_amount_frame_textbox.get()))
        self.add_ingredient_amount_frame_savebutt.grid(row = 5, column = 1,
                                                      sticky = "NESW")
        
        return self.add_ingredient_amount_frame
    
    def create_AddIngredientGenericTextFrame(self):
        '''If user chooses quantity type generic text, they will be placed on this frame'''
        self.add_ingredient_generic_text_frame = Frame(self.main_container)
        self.add_ingredient_generic_text_frame.grid(row = 0, column = 0,
                                                    sticky = "NESW")
        
        # Create and pack heading
        self.add_ingredient_generic_text_frame_heading = Label(self.add_ingredient_generic_text_frame,
                                                               text = "Enter text: ")
        self.add_ingredient_generic_text_frame_heading.grid(row = 0, column = 0,
                                                            sticky = "NESW")
        
        # Creates and packs textbox, where user can input whatever they need for the ingredient
        self.add_ingredient_generic_text_frame_textbox = Entry(self.add_ingredient_generic_text_frame)
        self.add_ingredient_generic_text_frame_textbox.grid(row = 1, column = 0,
                                                            sticky = "NESW")
        
        # Creates and packs next button
        
        # Creates and packs save button
        
                                                               
        
        return self.add_ingredient_generic_text_frame
    
# Main program
if __name__ == "__main__":
    app = Program()
    app.run()